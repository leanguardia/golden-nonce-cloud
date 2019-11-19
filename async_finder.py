from celery import Celery
from celery.result import ResultSet
from celery.task.control import inspect
import hashlib
import time

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

if __name__ == '__main__':
  data = "COMSM0010cloud"
  difficulty = 5
  N = 2
  golden_nonce = None
  scale = 10000
  batch = 0
  
  results = ResultSet([])
