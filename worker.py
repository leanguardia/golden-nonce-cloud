import datetime
from lib.sqs import Sqs
from lib.tasks_queue import TasksQueue
from app.nonce_evaluator import NonceEvaluator
import os

class Worker(object):
  def __init__(self):
    self.tasks_queue = TasksQueue()

  def run(self):
    sqs = Sqs()
    searching = True
    max_sequence_length = 32

    while(searching):
      tasks = self.tasks_queue.poll_tasks(max_attempts=5)
      if tasks:
        while(searching and tasks):
          task = tasks[0]
          nonce, search_to, difficulty, data = self.unwrap_task(task)
          print(task["Body"])
          
          while(searching and nonce <= search_to):
            binary_sequence = bin(nonce)[2:]
            
            while (searching and len(binary_sequence) <= max_sequence_length):
              evaluator = NonceEvaluator(data, binary_sequence, difficulty)
              if (evaluator.valid_nonce()):
                sqs.publish_golden_nonce(nonce, binary_sequence, evaluator.hexdigest)
                searching = False
              binary_sequence = "0" + binary_sequence
            nonce += 1

          self.tasks_queue.delete_message(task["ReceiptHandle"])
          stop_message = sqs.stop_search(max_retries=1)
          if stop_message != False: searching = False
          tasks = tasks[1:]
      else:
        print("No tasks to fulfill")
        searching = False
    # report what I've done
    print("I'm leaving, no purpose in life!")

  def unwrap_task(self, task):
    return (
      task["SearchFrom"],
      task["SearchTo"],
      task["Difficulty"],
      task["Data"]
    )

if __name__ == "__main__":
  print("Start searching at", datetime.datetime.now())
  Worker().run()
  print("Stoped searching at", datetime.datetime.now())
  # os.system("shutdown /s /t 1")