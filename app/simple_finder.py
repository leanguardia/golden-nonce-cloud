import hashlib
import time

class NonceFinder(object):
  def find(self, data, difficulty):
    golden_nonce = None
    nonce = 0
    while not golden_nonce:
      hash = self.__digest_hash(data, nonce)
      if self.__valid_hash(hash, difficulty):
        golden_nonce = nonce
      else:
        nonce = nonce + 1
    return (golden_nonce, hash)

  def __valid_hash(self, hash, difficulty):
    for i in range(difficulty):
      if hash[i] != '0': return False 
    return True

  def __digest_hash(self, data, nonce):
    block = (data + str(nonce)).encode("utf-8")
    return hashlib.sha256(block).hexdigest()

if __name__ == "__main__":
  data = "COMSM0010cloud"
  difficulty = 6
  start_time = time.time()
  golden_nonce, hash = NonceFinder().find(data, difficulty)
  processing_time = time.time() - start_time
  print("Difficulty: ", difficulty)
  print("Processing time: {0:.4f} s.".format(processing_time))
  print("Golden Nonce is", golden_nonce)
  print("Hash: ", hash)