import time, sys
from app import util
from app.nonce_evaluator import NonceEvaluator
from lib.sqs import Sqs
from remote.tasks_queue import TasksQueue
from remote.parallel_worker import ParallelWorker

class Cnd(object):
  def __init__(self, data, difficulty):
    self.data = data
    self.difficulty = difficulty
    self.tasks_queue = TasksQueue()
    
    self.batch_index = 0
    self.num_of_tests = 25000

  def direct_specification(self, num_of_vms, init_tasks, tasks_per_batch):
    print(f":: Direct Specification :: N = {num_of_vms}")
    self.tasks_queue.purge()
    sqs = Sqs()
    sqs.purge_stop_queue()
    threshold = 75

    num_of_batches = int(init_tasks / 10)
    self.send_batches(num_of_batches)

    parallel_worker = ParallelWorker(num_of_workers=num_of_vms)
    parallel_worker.run()
    parallel_worker.wait_initialization()

    num_of_batches = int(tasks_per_batch / 10)
    start_time = time.time()
    searching = True
    while searching:
      tasks_in_queue = self.tasks_queue.approx_num_of_tasks() # do this every now and then
      print("Tasks in queue:", tasks_in_queue)
      if tasks_in_queue < threshold:
        self.send_batches(num_of_batches)
      stop_message = sqs.stop_search(max_retries=15)
      if stop_message: searching = False

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
    
    statuses = parallel_worker.status()
    parallel_worker.shutdown()
    print("Sending Report ..")

  def send_batches(self, num_of_batches):
    print(f"Batch {self.batch_index} | {num_of_batches} tasks of size 10.")
    for index in range(num_of_batches):
      self.send_batch()

  def send_batch(self):
    response = self.tasks_queue.send_ten_tasks(self.data, self.difficulty, self.batch_index, self.num_of_tests)
    self.batch_index += 1

if __name__ == "__main__":
  n, difficulty, data = util.arguments(sys.argv)
  print("N:", n, "Data:", data, "| Difficulty:", difficulty)

  cnd = Cnd(data, difficulty)
  # cnd.send_batches()
  cnd.direct_specification(
    num_of_vms=n,
    init_tasks=100,
    tasks_per_batch=50,
  )