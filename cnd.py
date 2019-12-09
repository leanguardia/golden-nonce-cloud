import time
from worker import Worker
from lib.sqs import Sqs
from lib.tasks_queue import TasksQueue
from app.nonce_evaluator import NonceEvaluator

def unwrap_golden(message):
  return (
    task["SearchFrom"],
    task["SearchTo"],
    task["Difficulty"],
    task["Data"],
  )

# def send_tasks_batch(sqs, task_index, num_of_tests, num_of_tasks, difficulty, data):
#   start_time = time.time()
#   batch_number = int(task_index / num_of_tasks) + 1
#   starting_at = task_index * num_of_tests
#   tasks_per_batch = num_of_tasks * num_of_tests
#   ending_at = batch_number * tasks_per_batch - 1
#   for index in range(task_index, task_index + num_of_tasks):
#     search_from = index * num_of_tests
#     search_to = search_from + num_of_tests - 1
#     sqs.send_task(data, difficulty, (search_from, search_to))
#   print(f"Batch {batch_number} | {num_of_tasks} tasks of size {num_of_tests} from {starting_at} to {ending_at} in {time.time() - start_time} seconds.")
#   return task_index + num_of_tasks

if __name__ == "__main__":
  # difficulty, data = arguments(sys.argv)
  # print("Data:", data, "| Difficulty:", difficulty)

  data = 'COMSM0010cloud'
  difficulty = 7

  # SETUP QUEUES
  tasks_queue = TasksQueue()
  sqs = Sqs()
  # sqs.purge_all() # CREATE
  # sqs.purge_tasks_queue()
  

  # CREATE FIRST BATCH

  batch_index = 0
  num_of_tests = 10000
  threshold = 11

  num_of_tasks = 30
  num_of_batches = int(num_of_tasks / 10)

  print(f"Sending {num_of_batches} batches of 10 tasks")
  for index in range(num_of_batches):
    response = tasks_queue.send_ten_tasks(data, difficulty, batch_index, num_of_tests)
    batch_index += 1

  num_of_tasks = 20
  num_of_batches = int(num_of_tasks / 10)

  start_time = time.time()
  searching = True

  while searching:
    print("Check: N tasks")
    tasks_in_queue = tasks_queue.approx_num_of_tasks() # do this every now and then
    print("Tasks in queue:", tasks_in_queue)
    if tasks_in_queue < threshold:
      for index in range(num_of_batches):
        response = tasks_queue.send_ten_tasks(data, difficulty, batch_index, num_of_tests)
        batch_index += 1

    print("Check: Stop Queue")
    stop_message = sqs.stop_search(max_retries=1)
    if stop_message:
      searching = False

  processing_time = time.time() - start_time

  stop_reason = stop_message["StopReason"]
  print("-->", stop_reason)
  print(stop_message["Body"])
  if stop_reason == "NonceFound":
    nonce = stop_message["Nonce"]
    binary_sequence = stop_message["BinarySequence"]
    hexdigest = stop_message["Hexdigest"]
    print("Golden Nonce:", nonce, "|", binary_sequence +"("+ str(len(binary_sequence)) +")")
    print("Processing time: {0:.3f} s.".format(processing_time))
    print("Hexdigest", hexdigest)
  elif stop_reason == "EmergencyScram":
    print("Call 999!")
  
  sqs.delete_stop_message(stop_message["ReceiptHandle"])
  
  # sqs.purge_stop_queue()
  # sqs.purge_all()

  print("I'm useless xD")

