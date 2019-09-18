import json
import sqlite3
from contextlib import contextmanager

from flask import request

from crypto import *


@contextmanager
def database():
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    try:
        yield curs, conn
    finally:
        conn.close()


def decode_cookies(raise_exception=False):
    cookie = request.cookies.get('cookie')
    if not cookie:
        if raise_exception:
            abort(403)
        else:
            return None
    json_data = json.loads(AESCipher(AES_KEY).decrypt(cookie))
    username = json_data.get('username')
    return username
