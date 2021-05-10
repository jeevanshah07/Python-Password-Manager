"""
Credit to PyTutorials on Nitratine for the code snippets
https://nitratine.net/blog/post/encryption-and-decryption-in-python/
"""

from cryptography.fernet import Fernet
import os


def get_key():
    """
    Retrieves and/or writes the key needed for encryping and decryting items

    Returns: 
        str
    """

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
    """
    Encrypts a passed message using a key

    Args:
        message (str): The message or item that needs to be encrypted
        key (str): The Fernet encryption key 

    Returns:
        bytes: The encrypted message stored in bytes
    """

    message = str(message)
    message = bytes(message, 'utf8')

    encrypted = Fernet(key).encrypt(message)

    return encrypted


def decrypt(message, key):
    """
    Decrypts a passed message using a key

    Args:
        message (str or bytes): The message or item that needs to be decrypted
        key (str): The Fernet encryption key 

    Returns:
        str: The decrypted message stored in a string 
    """

    message = str(message)
    message = bytes(message, 'utf8')

    decrypted = Fernet(key).decrypt(message)

    return decrypted
