from pwn import *
from hashlib import sha512
from random import choice
from sympy.abc import x
from sympy import Poly
import string
import gmpy2

captcha_al = string.ascii_letters + string.digits

def inv(a, p):
    return int(gmpy2.invert(a, p))

r = remote("127.0.0.1", 33031)

r.readuntil("sha512(X)[:5] ==")
captcha = r.recvline().strip()

i = 0
while True:
    if sha512(str(i)).hexdigest()[:5] == captcha[:5]:
        break
    i += 1

r.sendline(str(i))

for step in range(50):

    r.recvuntil("N: ")
    n = int(r.recvline().strip())
    r.recvuntil("results: ")
    points = map(int, r.recvline().strip().split(','))
    p_x = points[0::2]
    p_y = points[1::2]   

    k = len(p_x) // 2
    p_x = p_x[:k]
    p_y = p_y[:k] 

    L = 0
    for j in range(k):
        l = 1
        for m in range(k):
            if j == m:
                continue
            l *= Poly(x - p_x[m]) * int(gmpy2.invert((p_x[j] - p_x[m]) % n, n))
        L += l * p_y[j]
    
    for chk in range(3):
        r.recvuntil("a = ")
        a = int(r.recvline().strip())
        b = L.eval(a) % n
        r.sendline(str(b))

    print "step", step + 1, "ok"

print r.recvall()