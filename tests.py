import hashlib

difficulty = 4
sha_encoder = hashlib.sha256()

def valid_hash(hash, difficulty):
  for i in range(0, difficulty):
    if hash[i] != '0': return False 
  return True

def digest_hash(data, nonce):
  sha_encoder.update((data + str(nonce)).encode('utf-8'))
  return sha_encoder.hexdigest()

golden_nonce = None
nonce = 0
while not golden_nonce:
  hash = digest_hash("COMSM0010", nonce)
  if valid_hash(hash, difficulty):
    golden_nonce = nonce
    print("Hash: ", hash)
  else:
    nonce = nonce + 1

print("The Golden Nonce is", golden_nonce)

#TODO: How long did it take?