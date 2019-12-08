import datetime
from lib.sqs import Sqs
from app.nonce_evaluator import NonceEvaluator

class Worker(object):
  def run(self):
    print("Start searching at", datetime.datetime.now())

    sqs = Sqs()
    searching = True
    max_sequence_length = 32

    while(searching):
      task = sqs.poll_task(max_retries=5)
      if task:
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

        sqs.delete_task_message(task["ReceiptHandle"])
        stop_message = sqs.stop_search(max_retries=2)
        if stop_message != False: searching = False
      else:
        print("No tasks to fulfill")
        searching = False
    # report what I've done
    print("Stoped searching at", datetime.datetime.now())

    print("I'm leaving, no purpose in life!")

  def unwrap_task(self, task):
    return (
      task["SearchFrom"],
      task["SearchTo"],
      task["Difficulty"],
      task["Data"]
    )

if __name__ == "__main__":
  worker = Worker()
  worker.run()