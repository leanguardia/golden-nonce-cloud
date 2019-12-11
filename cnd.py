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
    print(f":: Direct Specification :: N = {num_of_vms}")
    self.tasks_queue.purge()
    self.stop_queue.purge()

    threshold = 75

    num_of_batches = int(init_tasks / 10)
    self.send_batches(num_of_batches)

    parallel_worker = ParallelWorker(num_of_workers=num_of_vms)
    parallel_worker.run()
    parallel_worker.wait_initialization()

    num_of_batches = int(tasks_per_batch / 10)
    start_time = time.time()
    searching = True

    decision_index = 0
    while searching:
      if decision_index % 20 == 0:
        decision_index = 0
        available_tasks_count = self.tasks_queue.approx_num_of_tasks()
        print("Available tasks:", available_tasks_count)
        if available_tasks_count < threshold:
          self.send_batches(num_of_batches)
      
      stop_messages_count = self.stop_queue.approx_num_of_tasks()
      if stop_messages_count > 0: searching = False
      decision_index +=1 

    processing_time = time.time() - start_time
    
    statuses = parallel_worker.status()
    print(statuses)
    parallel_worker.shutdown()

    stop_message = self.poll_stop_message()

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

    print("Sending Report ..")

  def send_batches(self, num_of_batches):
    print(f"Batch {self.batch_index} | {num_of_batches} tasks of size 10.")
    for index in range(num_of_batches):
      self.send_batch()

  def send_batch(self):
    response = self.tasks_queue.send_ten_tasks(self.data, self.difficulty, self.batch_index, self.num_of_tests)
    self.batch_index += 1
  
  def poll_stop_message(self):
    print("Looking for results ...")
    stop_message = None
    while(not stop_message):
      stop_message = self.stop_queue.poll_stop_message(max_attempts=10)
    return stop_message

if __name__ == "__main__":
  n, difficulty, data = util.arguments(sys.argv)
  print("N:", n, "Data:", data, "| Difficulty:", difficulty)

  cnd = Cnd(data, difficulty)
  # cnd.send_batches()
  cnd.direct_specification(
    num_of_vms=n,
    init_tasks=100,
    tasks_per_batch=20,
  )