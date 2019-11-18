from cloudlibrary import NonceFinder
import time

if __name__ == "__main__":
  data = "COMSM0010cloud"
  difficulty = 5
  start_time = time.time()
  golden_nonce, hash = NonceFinder().find(data, difficulty)
  processing_time = time.time() - start_time
  print("Difficulty: ", difficulty)
  print("Processing time: {0:.4f} s.".format(processing_time))
  print("Golden Nonce is", golden_nonce)
  print("Hash: ", hash)
