import sys, getopt, time
from nonce_evaluator import NonceEvaluator 

class NonceFinder(object):
  def find_by_zero_prepend(self, data, difficulty):
    golden_nonce = None
    max_sequence_length = 32
    nonce = 0
    while (not golden_nonce):
      binary_sequence = self.binary_format(nonce)
      while (not golden_nonce and len(binary_sequence) <= max_sequence_length):
        evaluator = NonceEvaluator(data, binary_sequence, difficulty)
        if (evaluator.valid_nonce()): golden_nonce = binary_sequence
        binary_sequence = "0" + binary_sequence
      nonce += 1
    return (golden_nonce, evaluator.hexdigest)

  def find_by_increment(self, data, difficulty):
    golden_nonce = None
    sequence_length = 1
    max_sequence_length = 32
    while (not golden_nonce and sequence_length <= max_sequence_length):
      upper_limit = 2 ** sequence_length
      nonce = 0
      while (not golden_nonce and nonce < upper_limit):
        binary_sequence = self.binary_format(nonce, sequence_length).rjust(sequence_length, '0')
        # print(sequence_length, nonce, binary_sequence)
        evaluator = NonceEvaluator(data, binary_sequence, difficulty)
        if (evaluator.valid_nonce()):
          golden_nonce = binary_sequence
        nonce += 1
      sequence_length += 1
      print(sequence_length, upper_limit, "trails")
    return (golden_nonce, evaluator.hexdigest)

  def binary_format(self, nonce):
    return bin(nonce)[2:]

def arguments(argv, difficulty=None, data="COMSM0010cloud"):
  try: opts, args = getopt.getopt(argv[1:], "hd:a:", ["difficulty=","data="])
  except getopt.GetoptError:
    print('simple_finder.py -d <difficulty> -a <data>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('simple_finder.py -d <difficulty> -a <data>')
      sys.exit()
    elif opt in ("-d", "--difficulty"): difficulty = int(arg)
    elif opt in ("-a", "--data"): data = arg
  return (difficulty, data) 

if __name__ == "__main__":
  difficulty, data = arguments(sys.argv)
  print("Data:", data, "| Difficulty:", difficulty)

  start_time = time.time()
  binary_sequence, hexdigest = NonceFinder().find_by_zero_prepend(data, difficulty)
  processing_time = time.time() - start_time
  nonce = int(binary_sequence, 2)
  print("Golden Nonce:", nonce, "|", binary_sequence +"("+str(len(binary_sequence))+")")
  print("Processing time: {0:.3f} s.".format(processing_time))
  print("Hexdigest", hexdigest)

# TODO: CHANGE EVALUATOR TO CHECK BITS, NO HEX DIGITS