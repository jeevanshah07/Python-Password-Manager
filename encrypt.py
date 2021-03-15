'''
Credit to SamG101 on stackoverflow for the code
https://stackoverflow.com/questions/44223479/how-to-use-rsa-or-similar-encryption-in-python-3


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


cipher = RSA_Cipher()
cipher.generate_key(1024) #key length can be 1024, 2048 or 4096
'''

'''
https://nitratine.net/blog/post/encryption-and-decryption-in-python/#encrypting
'''
import bcrypt
import mysql.connector


# db = mysql.connector.connect(
#     host="192.168.86.5", user="root", passwd="starwars285", db="passwordManager"
# )

# c = db.cursor()

# c.execute("SELECT password FROM passwords WHERE id=1")
# print(c)
# for i in c:
# 	passwd = bytes(str(i), 'utf8')

# hashed = bcrypt.hashpw(passwd, bcrypt.gensalt(rounds=15))
# print(hashed)

# if bcrypt.checkpw(passwd, hashed):
# 	print("Match")
# else:
# 	print("Not a match")
from cryptography.fernet import Fernet
import os

def get_key():
	with open('key.key', 'r+b') as f:
		key = Fernet.generate_key()	
		if os.path.getsize('key.key') == 0:
			f.write(key)
		else:
			key = f.read()
		
	return key

def encrypt(message, key):
	message = str(message)
	message = bytes(message, 'utf8')
	
	encrypted = Fernet(key).encrypt(message) 

	return encrypted

def decrypt(message, key):
	message = str(message)
	message = bytes(message, 'utf8')
	
	decrypted = Fernet(key).decrypt(message)

	return decrypted

# string = "hello world"

# key = get_key()
# print(key)
# encrypted = encrypt(string, key)
# print(encrypted)
# decrypted = decrypt(encrypted, key)
# print(decrypted)