import time, sys
from app import util
from app.nonce_evaluator import NonceEvaluator
from remote.tasks_queue import TasksQueue
from remote.stop_queue import StopQueue
from remote.parallel_worker import ParallelWorker

class Cnd(object):
  def __init__(self, data, difficulty):
    self.data = data
    self.difficulty = difficulty
    self.tasks_queue = TasksQueue()
    self.stop_queue = StopQueue()
    
    self.batch_index = 0
    self.num_of_tests = 25000

  def direct_specification(self, num_of_vms, init_tasks, tasks_per_batch):
    self.report_search(num_of_vms)
    parallel_worker = ParallelWorker(num_of_workers = num_of_vms)
    parallel_worker.run()

    self.tasks_queue.purge()
    self.stop_queue.purge()

    min_available_tasks = 80

    num_of_batches = int(init_tasks / 10)
    self.send_batches(num_of_batches)

    num_of_batches = int(tasks_per_batch / 10)
    searching = True

    decision_index = 0
    parallel_worker.wait_initialization()

    start_time = time.time()
    while searching:
      if decision_index % 25 == 0:
        decision_index = 0
        available_tasks_count = self.tasks_queue.approx_num_of_tasks()
        print("Available tasks:", available_tasks_count)
        if available_tasks_count < min_available_tasks:
          self.send_batches(num_of_batches)
      if self.stop_queue.stop(): searching = False
      decision_index +=1 

    processing_time = time.time() - start_time
    print("Processing time: {0:.3f} seconds".format(processing_time))

    parallel_worker.shutdown()

    self.report_stop(self.poll_stop_message())

  def send_batches(self, num_of_batches):
    for index in range(num_of_batches):
      self.send_batch()

  def send_batch(self):
    print(f"Batch {self.batch_index} | 10 tasks of size {self.num_of_tests} each.")
    response = self.tasks_queue.send_ten_tasks(self.data, self.difficulty, self.batch_index, self.num_of_tests)
    self.batch_index += 1
  
  def poll_stop_message(self):
    stop_message = None
    while(not stop_message):
      stop_message = self.stop_queue.poll_stop_message(max_attempts=10)
    return stop_message

  def report_stop(self, stop_message):
    print(stop_message["Body"])
    stop_reason = stop_message["StopReason"]
    print("-->", stop_reason)
    if stop_reason == "NonceFound":
      self.report_golden_nonce(stop_message)
    elif stop_reason == "EmergencyScram":
      print("Call 999!")

    print("Sending Report ..")

  def report_search(self, num_of_vms):
    print("Direct Specification Search:")
    print(" - Data:", self.data)
    print(" - Difficulty:", self.difficulty)
    print(" - Workers:", num_of_vms)

  def report_golden_nonce(self, stop_message):
    nonce = stop_message["Nonce"]
    binary_sequence = stop_message["BinarySequence"]
    print("Data:", data, "| Difficulty:", difficulty)
    print("Golden Nonce:", nonce, "|", binary_sequence +"("+ str(len(binary_sequence)) +")")
    print("Hexdigest", stop_message["Hexdigest"])

if __name__ == "__main__":
  n, difficulty, data = util.arguments(sys.argv)

  cnd = Cnd(data, difficulty)
  # cnd.send_batches()
  cnd.direct_specification(
    num_of_vms = n,
    init_tasks = 120,
    tasks_per_batch = 20,
  )