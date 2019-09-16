import os
from base64 import b64decode
from base64 import b64encode
from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES
from flask import abort, make_response

AES_KEY = md5(os.urandom(16)).hexdigest()

BLOCK_SIZE = 16  # Bytes


def check_padding(s):
    need_padding = bytes([s[-1]] * s[-1])
    if s[-len(need_padding):] != need_padding:
        abort(make_response("Invalid padding", 400))


def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s):
    check_padding(s)
    return s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = cipher.decrypt(enc[16:])
        return unpad(data).decode('utf8')
