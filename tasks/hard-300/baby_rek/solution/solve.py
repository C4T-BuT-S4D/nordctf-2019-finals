from pwn import *
from hashlib import sha512
from random import choice
import string
import gmpy2

captcha_al = string.ascii_letters + string.digits

def inv(a, p):
    return int(gmpy2.invert(a, p))

r = remote("127.0.0.1", 33061)

r.readuntil("sha512(X)[:5] ==")
captcha = r.recvline().strip()

i = 0
while True:
    if sha512(str(i)).hexdigest()[:5] == captcha[:5]:
        break
    i += 1

r.sendline(str(i))

for step in range(50):

    r.recvuntil("f1(x) =")
    s = r.recvline().strip().split(' ')
    A = int(s[0])
    B = int(s[4])
    r.recvuntil("f2(x) =")
    s = r.recvline().strip().split(' ')
    C = int(s[0])
    D = int(s[4])
    r.recvuntil("a = ")
    a = int(r.recvline().strip())
    r.recvuntil("n = ")
    p = int(r.recvline().strip())
    r.recvline()

    ans = int(
        a*inv(A, p) +\
        p*(
            p*inv(C, p - 1) -\
            a*inv(A, p) +\
            B*inv(A, p) -\
            D*inv(C, p - 1)
        ) -\
        B*inv(A, p)
    )

    r.sendline(str(ans))

    print "step", step + 1, "ok"

print r.recvall()