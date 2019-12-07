import hashlib

class NonceEvaluator(object):
  def __init__(self, data, binary_sequence, difficulty):
    self.data = data
    self.binary_sequence = binary_sequence
    self.difficulty = difficulty
    self.sha_squared = self.__sha_squared()
    self.hexdigest = self.sha_squared.hexdigest()

  def valid_nonce(self):
    for i in range(self.difficulty):
      if self.hexdigest[i] != '0': return False
    return True

  def nonce(self):
    return (int(self.binary_sequence, 2), self.binary_sequence)

  def __sha_squared(self):
    block = (self.data + self.binary_sequence).encode("utf-8")
    sha_1 = hashlib.sha256(block)
    return hashlib.sha256(sha_1.digest())

if __name__ == '__main__':
  data = "COMSM0010cloud"
  binary_sequence = "000"
  difficulty = 2

  evaluator = NonceEvaluator(data, binary_sequence, difficulty)

  print(evaluator.sha_squared.digest_size, "bytes")
  print("Hexdigest:", evaluator.hexdigest)
  print("Valid:", evaluator.valid_nonce())
  nonce, binary_representation = evaluator.nonce()
  print("Nonce (int):", nonce)
  print("Nonce (binary):", binary_representation)
