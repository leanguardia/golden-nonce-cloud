import time
from lib.sqs import Sqs
from app.nonce_evaluator import NonceEvaluator

def unwrap_task(task):
  return (
    task["SearchFrom"],
    task["SearchTo"],
    task["Difficulty"],
    task["Data"]
  )

def unwrap_golden(message):
  return (
    task["SearchFrom"],
    task["SearchTo"],
    task["Difficulty"],
    task["Data"],
  )

if __name__ == "__main__":
  # difficulty, data = arguments(sys.argv)
  # print("Data:", data, "| Difficulty:", difficulty)

  data = 'COMSM0010cloud'
  difficulty = 5
  sqs = Sqs()
  sqs.purge_all()
  
  batch_size = 10000
  num_of_tasks = 10

  for task_index in range(num_of_tasks):
    search_from = task_index * batch_size
    search_to = search_from + batch_size - 1
    print("Sending:", search_from, search_to)
    sqs.send_task(data, difficulty, (search_from, search_to))

  searching = True
  start_time = time.time()
  max_sequence_length = 32

  while(searching):
    task = sqs.poll_task(max_retries=3)
    if task:
      nonce, search_to, difficulty, data = unwrap_task(task)
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

      sqs.delete_message(task["ReceiptHandle"])
      stop_message = sqs.stop_search(max_retries=2)
      if stop_message != False: searching = False
    else:
      print("No tasks to fulfill")
      searching = False
  
  processing_time = time.time() - start_time
  print(stop_message["Body"])
  if stop_message["StopReason"] == "NonceFound":
    nonce = stop_message["Nonce"]
    binary_sequence = stop_message["BinarySequence"]
    hexdigest = stop_message["Hexdigest"]

    print("Golden Nonce:", nonce, "|", binary_sequence +"("+ str(len(binary_sequence)) +")")
    print("Processing time: {0:.3f} s.".format(processing_time))
    print("Hexdigest", hexdigest)
  
  sqs.delete_message(task["ReceiptHandle"])
  # sqs.purge_stop_queue()
  # sqs.purge_all()

  print("I'm useless xD")

