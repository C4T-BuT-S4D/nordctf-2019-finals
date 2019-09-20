from sympy import groebner, Poly
from sympy.parsing.sympy_parser import parse_expr

f = open("task.txt", "r")
s = f.readlines()
f.close()

k = s[1].strip()[6:-1].split(', ')

key = [Poly(i) for i in k]

F = groebner(key)

res = ""

for i in range(2, len(s)):
    p = parse_expr(s[i].strip())
    r = F.contains(p)
    if r:
        res += "1"
    else:
        res += "0"

print(''.join(chr(int(res[i:i+8], 2)) for i in range(0, len(res), 8)))