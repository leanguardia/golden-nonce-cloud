import time
from worker import Worker
from lib.sqs import Sqs
from lib.tasks_queue import TasksQueue
from app.nonce_evaluator import NonceEvaluator

class Cnd(object):
  def __init__(self, data, difficulty):
    self.data = data
    self.difficulty = difficulty
    self.tasks_queue = TasksQueue()
    
    self.batch_index = 0
    self.num_of_tests = 10000

  def direct_specification(self, num_of_vms):
    print(f":: Direct Specification :: N = {num_of_vms}")
    sqs = Sqs()
    # sqs.purge_all()
    sqs.purge_tasks_queue()

    num_of_tasks = 30
    threshold = 11

    num_of_batches = int(num_of_tasks / 10)
    self.send_batches(num_of_batches)

    num_of_tasks = 20
    num_of_batches = int(num_of_tasks / 10)

    start_time = time.time()
    searching = True
    while searching:
      print("Check: N tasks")
      tasks_in_queue = self.tasks_queue.approx_num_of_tasks() # do this every now and then
      print("Tasks in queue:", tasks_in_queue)
      if tasks_in_queue < threshold:
        self.send_batches(num_of_batches)

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

  def send_batches(self, num_of_batches):
    print(f"Sending {num_of_batches} batches of 10 tasks")
    # print(f"Batch {batch_number} | {num_of_tasks} tasks of size {num_of_tests} from {starting_at} to {ending_at} in {time.time() - start_time} seconds.")
    for index in range(num_of_batches):
      self.send_batch()

  def send_batch(self):
    response = self.tasks_queue.send_ten_tasks(self.data, self.difficulty, self.batch_index, self.num_of_tests)
    self.batch_index += 1

if __name__ == "__main__":
  # difficulty, data = arguments(sys.argv)
  # print("Data:", data, "| Difficulty:", difficulty)

  data = 'COMSM0010cloud'
  difficulty = 6

  cnd = Cnd(data, difficulty)
  cnd.direct_specification(1) #