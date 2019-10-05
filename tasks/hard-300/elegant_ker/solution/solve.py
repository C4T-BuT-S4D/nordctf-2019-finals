from sympy.abc import x
from sympy import Poly, factor
from numpy.linalg import inv

s = open("encrypted.txt", "r").read().strip()

blocks = s.split(':')

M = [
        [3, 5, 1, 9, 4, 2, 3],
        [5, 3, 0, 5, 9, 7, 7],
        [4, 0, 0, 6, 3, 8, 2],
        [9, 5, 6, 0, 3, 1, 1],
        [4, 9, 3, 3, 3, 0, 5],
        [2, 7, 8, 4, 0, 4, 4],
        [3, 7, 6, 1, 5, 4, 8],
    ]

M = inv(M)

for b in blocks:

    c = b.split('+')

    c = list(map(lambda x: int(x.split('*')[0]), c))

    a = 0
    for i in c:
        a *= x
        a += i

    a = Poly(a)

    a = str(factor(a))[1:-4]
    a = a.split(' + ')
    
    a = list(map(lambda x: int(x.split('*')[0]), a))[::-1]

    a = a @ M @ M @ M
    for i in range(7):
        if a[i] > 2:
            print(chr(int(round(a[i]))), end='')
