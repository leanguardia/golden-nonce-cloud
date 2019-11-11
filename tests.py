import hashlib
import time

def valid_hash(hash, difficulty):
  for i in range(difficulty):
    if hash[i] != '0': return False 
  return True

def digest_hash(data, nonce):
  block = (data + str(nonce)).encode("utf-8")
  return hashlib.sha256(block).hexdigest()

def find_golden_nonce(data, difficulty):
  golden_nonce = None
  nonce = 0
  while not golden_nonce:
    hash = digest_hash(data, nonce)
    if valid_hash(hash, difficulty):
      golden_nonce = nonce
    else:
      nonce = nonce + 1
  return (golden_nonce, hash)

# MAIN

data = "COMSM0010cloud"
difficulty = 7
start_time = time.time()
golden_nonce, hash = find_golden_nonce(data, difficulty)
processing_time = time.time() - start_time
print("Processing time: {0:.2f} s.".format(processing_time))
print("The Golden Nonce is", golden_nonce)
print("Hash: ", hash)