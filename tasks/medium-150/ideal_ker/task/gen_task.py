from sympy import groebner
from sympy.abc import x, y, z
from random import randint

key = [
    x**3 + x**2 * y + z,
    x * y * z + y**2 * z + x * z,
    x * y * z,
    x + z,
]

F = groebner(key)

flag = "flag{not_rly_ideal_ker_mmmm}"
flag_enc = ""

for i in flag:
    flag_enc += bin(ord(i))[2:].zfill(8)

f = open("task.txt", "w")
f.write("I thought it would be an ideal task\n")
f.write(f"key: {str(key)}\n")

for i in flag_enc:
    if i == '1':
        want = True
    else:
        want = False
    r = None
    while r != want:
        l = randint(5, 10)
        poly = 0
        for i in range(l):
            k = randint(-10, 10)
            a = randint(0, 10)
            b = randint(0, 10)
            c = randint(0, 10)
            poly += k * x**a * y**b * z**c

        r = F.contains(poly)
    f.write(f"{str(poly)}\n")

f.close()