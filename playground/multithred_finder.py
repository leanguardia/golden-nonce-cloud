import hashlib
import time
from multiprocessing import Process, Value

def valid_hash(hash, difficulty):
    for i in range(difficulty):
      if hash[i] != '0': return False 
    print("Golden Nonce Found!")
    return True

def digest_hash(data, nonce):
  block = (data + str(nonce)).encode("utf-8")
  return hashlib.sha256(block).hexdigest()

def find(data, difficulty, ranch, golden):
  for nonce in ranch:
    hash = digest_hash(data, nonce)
    if valid_hash(hash, difficulty):
      golden.value = nonce
      break


if __name__ == "__main__":
  data = "COMSM0010cloud"
  golden_nonce = Value('d', -1)
  processes = []
  index = 0
  difficulty = 6
  machines = 2

  start_time = time.time()
  while golden_nonce.value == -1:
    for i in range(0, machines):
      scale = 1000
      ranch = range(index * scale, index * scale + scale)
      process = Process(target=find, args=(data, difficulty, ranch, golden_nonce))
      # print("starting", index)
      process.start()
      processes.append(process)
      index = index + 1

    for process in processes:
      process.join()
  
  processing_time = time.time() - start_time

  print("Difficulty: ", difficulty)
  print("Processing time: {0:.4f} s.".format(processing_time))
  print("Golden Nonce is", golden_nonce.value)
  print("Hash: ", hash)
