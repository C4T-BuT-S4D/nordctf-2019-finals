from PIL import Image, ImageDraw
from copy import deepcopy

def multiply(A, v):
    res = [0 for _ in range(len(v))]
    for i in range(len(A)):
        for j in range(len(v)):
            res[i] = (res[i] + A[i][j] * v[j]) % M
    return res

def mult(A, B):
    D = [[0 for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            for t in range(5):
                D[i][j] = (D[i][j] + A[i][t] * B[t][j]) % M
    return D

img = Image.open("encoded.png")
w, h = img.size
pix = img.load()

M = w * h
A = [
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]
state = [1, 1, 1, 1, 1]

def pw(A, p):
    if p == 1:
        return A
    if p % 2 == 0:
        C = pw(A, p // 2)
        return mult(C, C)
    return mult(A, pw(A, p - 1))

def get():
    global state
    state = state[1:] + [sum(state)]
    return state[-1] % M

begin = pow(10, 100)

state = multiply(pw(A, begin), state)

positions = []

for i in range(w):
    for j in range(h):
        positions.append((i, j))

flag = ""

for i in range(29):
    pos = positions[get()]
    x, y = pos
    flag += chr(pix[x, y][0])

print(flag)