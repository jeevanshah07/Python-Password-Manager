"""
Credit to PyTutorials on Nitratine for the code snippets
https://nitratine.net/blog/post/encryption-and-decryption-in-python/
"""

from cryptography.fernet import Fernet
import os


def get_key():
    if os.path.exists('data/key.key'):
        with open('data/key.key', 'r+b') as f:
            key = Fernet.generate_key()
            if os.path.getsize('data/key.key') == 0:
                f.write(key)
            else:
                key = f.read()
    else:
        with open('data/key.key/', 'r+b') as f:
            key = Fernet.generate_key()
            f.write(key)
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
