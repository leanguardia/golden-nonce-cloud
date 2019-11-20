from collections import deque
import hashlib
import time
from celery import Celery
from celery.result import ResultSet
from celery.task.control import inspect

broker_url = 'amqp://guest:guest@localhost:5672'
app = Celery('async_finder', broker=broker_url, backend='rpc://')

def valid_hash(hash, difficulty):
    for i in range(difficulty):
      if hash[i] != '0': return False 
    return True

def digest_hash(data, nonce):
  block = (data + str(nonce)).encode("utf-8")
  return hashlib.sha256(block).hexdigest()

@app.task
def find(data, difficulty, batch, start, end):
  print(f"Batch {batch}: {start} to {end}")
  for nonce in range(start, end):
    hash = digest_hash(data, nonce)
    if valid_hash(hash, difficulty):
      print(f"Golden Nonce Found!: {nonce}")
      return nonce
      break
  return None

def sched_task(data, difficulty, index, scale=10000):
  start = index * scale
  end = start + scale
  return find.delay(data, difficulty, batch, start, end)

def values(results):
  values = []
  for result in results:
    if result.status == 'SUCCESS':
      values.append(result.result)
    else:
      values.append('N/A')
  return values

def get_nonce(results):
  for result in results:
    if result.status == 'SUCCESS' and result.get() != None:
      return result.result
  return None

if __name__ == '__main__':
  data = "COMSM0010cloud"
  difficulty = 8
  N = 1
  golden_nonce = None
  scale = 10000000
  batch = 0
  results = deque()

  start_time = time.time()
  
  for i in range(N + 20):
    results.append(sched_task(data, difficulty, batch, scale))
    batch += 1

  while(not golden_nonce):
    finished = 0
    for result in results:
      if result.status == 'SUCCESS':
        finished += 1; break
    golden_nonce = get_nonce(results)
    for i in range(finished):
      results.popleft()
      results.append(sched_task(data, difficulty, batch, scale))
      batch += 1

  processing_time = time.time() - start_time
  print("Difficulty: ", difficulty)
  print("N of machines: ", N)
  print("Processing time: {0:.4f} s.".format(processing_time))
  print("Golden Nonce is", golden_nonce)
