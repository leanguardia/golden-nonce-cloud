import time
from nonce_evaluator import NonceEvaluator 

class NonceFinder(object):
  def find(self, data, difficulty):
    golden_nonce = None
    sequence_length = 1
    max_sequence_length = 32
    while (not golden_nonce and sequence_length <= max_sequence_length):
      upper_limit = 2 ** (sequence_length)
      nonce = 0
      while (not golden_nonce and nonce < upper_limit):
        binary_sequence = self.format_sequence(nonce, sequence_length)
        # print(sequence_length, nonce, binary_sequence)
  
        evaluator = NonceEvaluator(data, binary_sequence, difficulty)
        if (evaluator.valid_nonce()):
          golden_nonce = binary_sequence
        nonce +=1
      sequence_length += 1
      print(sequence_length, upper_limit, "trails")
    return (golden_nonce, evaluator.hexdigest)

  def format_sequence(self, nonce, sequence_length):
    return bin(nonce)[2:].rjust(sequence_length, '0')

if __name__ == "__main__":
  data = "COMSM0010cloud"
  difficulty = 7
  start_time = time.time()

  binary_sequence, hexdigest = NonceFinder().find(data, difficulty)
  processing_time = time.time() - start_time
  print("Difficulty: ", difficulty)
  print("Processing time: {0:.4f} s.".format(processing_time))
  print("Golden Nonce (Integer):", int(binary_sequence, 2))
  print("Golden Nonce (Binary):", binary_sequence)
  print("Length: ", len(binary_sequence))
  print("Hexdigest", hexdigest)