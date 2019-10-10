#!/usr/bin/env python3

from Crypto.Util.number import getPrime
from random import randint, choices
from hashlib import sha512
import string

flag = open("flag.txt").read()

def solve(tasks, inp, n):
    c_tasks = tasks[::-1]
    ret = 0
    for i in range(len(c_tasks)):
        ret = (ret + pow(inp, i, n) * c_tasks[i]) % n
    return ret

def get_task():
    n = getPrime(128)
    k = randint(5, 50)
    tasks = [randint(0, n - 1) for _ in range(k)]
    tasks[0] = 1
    tmp = [randint(0, n - 1) for _ in range(2 * k)]
    results = [(i, solve(tasks, i, n)) for i in tmp]

    return n, tasks, results

print("Complete captcha to get access to the task")
captcha_al = string.ascii_letters + string.digits
captcha_text = ''.join(choices(captcha_al, k=4))
captcha = sha512(captcha_text.encode()).hexdigest()
print(captcha_text)
print(f"sha512(X)[:5] == {captcha[:5]}")

captcha_check = input().strip()

if sha512(captcha_check.encode()).hexdigest()[:5] != captcha[:5]:
    print("Incorrect captcha!")
    exit(0)

print("""Welcome to the kerrest game ever!
To get to the next stage you have to solve the following questions:""")

for i in range(50):
    n, tasks, results = get_task()

    print(f"""N: {n}
results: {','.join(map(lambda res: f"{res[0]},{res[1]}", results))}
Find that guy!!1!""")

    for chk in range(3):
        a = randint(0, n - 1)
        print(f"a = {a}\nAnswer: ")
        x = int(input().strip())
        if x == solve(tasks, a, n):
            print("OK")
        else:
            print("BAD")
            exit(0)

print(flag)