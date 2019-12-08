from lib.sqs import Sqs
from app.nonce_evaluator import NonceEvaluator

def unwrap_task(task):
  return (
    task["SearchFrom"],
    task["SearchTo"],
    task["Difficulty"],
    task["Data"]
  )

if __name__ == "__main__":
  # difficulty, data = arguments(sys.argv)
  # print("Data:", data, "| Difficulty:", difficulty)

  # start_time = time.time()
  sqs = Sqs()
  # sqs.purge_all()

  # create_tasks

  searching = True
  found = False
  while(searching and not found):
    task = sqs.next_task(max_retries=3)
    if task:
      nonce, search_to, difficulty, data = unwrap_task(task)
      print(task["Body"])
      while(not found and nonce <= search_to):
        binary_sequence = bin(nonce)[2:]
        evaluator = NonceEvaluator(data, binary_sequence, difficulty)
        if(evaluator.valid_nonce()):
          sqs.publish_golden_nonce(nonce, binary_sequence)
        nonce += 1
      sqs.complete_task(task)
      stop_message = sqs.stop_search()
      if stop_message != None: searching = False
    else:
      print("No tasks to fulfill")
      searching = False


  print("I'm useless xD")
