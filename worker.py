import datetime
import os
import logging
from remote.tasks_queue import TasksQueue
from remote.stop_queue import StopQueue
from app.nonce_evaluator import NonceEvaluator

LOG_FORMAT = "%(levelname)s %(message)s"
logging.basicConfig(
  filename = "worker.log",
  level = logging.INFO,
  format = LOG_FORMAT,
  filemode='w',
)
logger = logging.getLogger()

class Worker(object):
  def __init__(self):
    self.tasks_queue = TasksQueue()
    self.stop_queue = StopQueue()

  def run(self):
    searching = True
    max_sequence_length = 32

    while(searching):
      tasks = self.tasks_queue.poll_tasks(max_attempts=1, wait_time_seconds=1)
      msj = f"Retrieved {len(tasks)} tasks"; print(msj); logger.info(msj)
      logger.info(f"Retrieved {len(tasks)} tasks")
      while(searching and tasks):
        task = tasks[0]
        nonce, search_to, difficulty, data = self.unwrap_task(task)

        print(task['Body'])
        logger.info(task['Body'])
        while(searching and nonce <= search_to):
          binary_sequence = bin(nonce)[2:]
          
          while (searching and len(binary_sequence) <= max_sequence_length):
            evaluator = NonceEvaluator(data, binary_sequence, difficulty)
            if (evaluator.valid_nonce()):
              print("Golden Nonce:", nonce, "|", binary_sequence +"("+ str(len(binary_sequence)) +")")
              self.stop_queue.send_golden_nonce(nonce, binary_sequence, evaluator.hexdigest)
              searching = False
            binary_sequence = "0" + binary_sequence
          nonce += 1

        self.tasks_queue.delete_message(task["ReceiptHandle"])

        if self.stop_queue.stop(): searching = False
        tasks = tasks[1:]
    
    print("Stopped searching")
    # report what I've done

  def unwrap_task(self, task):
    return (
      task["SearchFrom"],
      task["SearchTo"],
      task["Difficulty"],
      task["Data"]
    )

if __name__ == "__main__":
  logger.info("Worker starting at " + str(datetime.datetime.now()))
  Worker().run()
  logger.info("Worker stopping at " + str(datetime.datetime.now()))