'''
Credit to SamG101 on stackoverflow for the code
https://stackoverflow.com/questions/44223479/how-to-use-rsa-or-similar-encryption-in-python-3
'''

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random
from base64 import b64encode
from base64 import b64decode

class RSA_Cipher:
  def generate_key(self,key_length):
    assert key_length in [1024,2048,4096]
    rng = Random().read
    self.key = RSA.generate(key_length,rng)

  def encrypt(self,data):
    plaintext = b64encode(data.encode())
    rsa_encryption_cipher = PKCS1_v1_5.new(self.key)
    ciphertext = rsa_encryption_cipher.encrypt(plaintext)
    return b64encode(ciphertext).decode()

  def decrypt(self,data):
    ciphertext = b64decode(data.encode())
    rsa_decryption_cipher = PKCS1_v1_5.new(self.key)
    plaintext = rsa_decryption_cipher.decrypt(ciphertext,16)
    return b64decode(plaintext).decode()

'''
cipher = RSA_Cipher()
cipher.generate_key(1024) #key length can be 1024, 2048 or 4096
encryption = cipher.encrypt("hello world")
print(encryption)
encryption = cipher.decrypt(encryption)
print(encryption)
'''