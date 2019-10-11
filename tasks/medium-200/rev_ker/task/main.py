#!/usr/bin/env python3

from Crypto.Util.number import getPrime
from random import randint, choices
from hashlib import sha512
import string

flag = open("flag.txt").read()

def check(x, a, n, A, B, C, D):
    return pow(A * x + B, (C * x + D) % (n - 1), n) == a

def get_task():
    n = getPrime(1024)
    a = randint(0, n - 1)
    A = getPrime(512)
    B = getPrime(512)
    C = getPrime(512)
    D = getPrime(512)

    return a, n, A, B, C, D

print("Complete captcha to get access to the task")
captcha_al = string.ascii_letters + string.digits
captcha_text = ''.join(choices(captcha_al, k=4))
captcha = sha512(captcha_text.encode()).hexdigest()
print(f"sha512(X)[:5] == {captcha[:5]}")

captcha_check = input().strip()

if sha512(captcha_check.encode()).hexdigest()[:5] != captcha[:5]:
    print("Incorrect captcha!")
    exit(0)

print("""Welcome to ker archives!
To get to the next stage you have to solve the following questions:""")

for i in range(50):
    a, n, A, B, C, D = get_task()

    print(f"""Find x such that pow(f1(x), f2(x), n) == a
Where
f1(x) = {A} * x + {B}
f2(x) = {C} * x + {D}""")

    print(f"a = {a}\nn = {n}\nAnswer: ")
    x = int(input().strip())
    if check(x, a, n, A, B, C, D):
        print("OK")
    else:
        print("BAD")
        exit(0)

print(flag)
