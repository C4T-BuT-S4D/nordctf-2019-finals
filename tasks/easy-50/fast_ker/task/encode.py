from PIL import Image, ImageDraw

flag = open("flag.txt").read()
img = Image.open("image.png")
w, h = img.size
pix = img.load()

M = w * h
state = [1, 1, 1, 1, 1]

def get():
    global state
    state = state[1:] + [sum(state)]
    return state[-1] % M

used = set()

begin = pow(10, 100)

for i in range(begin):
    get()

positions = []

for i in range(w):
    for j in range(h):
        positions.append((i, j))

draw = ImageDraw.Draw(img)

for i in range(len(flag)):
    pos = positions[get()]
    x, y = pos
    draw.point(pos, (ord(flag[i]), pix[x, y][1], pix[x, y][2]))
    used.add(pos)

assert len(used) == len(flag)

img.save("encoded.png")