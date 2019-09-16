import os
from base64 import b64encode
from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES

AES_KEY = md5(os.urandom(16)).hexdigest()

BLOCK_SIZE = 16  # Bytes


def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        enc = cipher.encrypt(raw)
        return b64encode(iv + enc)
