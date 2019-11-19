from celery import Celery, result
import hashlib
import time

broker_url = 'amqp://guest:guest@localhost:5672'
app = Celery('async_finder', broker=broker_url, backend='rpc://')

def valid_hash(hash, difficulty):
    for i in range(difficulty):
      if hash[i] != '0': return False 
    print("Golden Nonce Found!")
    return True

def digest_hash(data, nonce):
  block = (data + str(nonce)).encode("utf-8")
  return hashlib.sha256(block).hexdigest()

@app.task
def find(data, difficulty, start, end):
  print(f"Testing from: {start} to {end}")
  for nonce in range(start, end):
    hash = digest_hash(data, nonce)
    if valid_hash(hash, difficulty):
      print(f"Golden Nonce Found!: {nonce}")
      return nonce
      break
  print("Nothing found")
  return None

if __name__ == '__main__':
  data = "COMSM0010cloud"
  difficulty = 6
  index = 0
  machines = 75
  results = result.ResultSet([])
  golden_nonce = None
  # while golden_nonce == None:
  for machine in range(machines):
    scale = 100000
    start = index * scale
    end = (index * scale) + scale
    ranch = range(start, end)
    async_result = find.delay(data, difficulty, start, end)
    results.add(async_result)
    index = index + 1

  print("results", results.join())
