from pwn import *
from binascii import unhexlify

io = process('./main')
bitmap = io.recvuntil('\n')[:-1]

bitmap = hex(int(bitmap, 2))[2:]
print unhexlify(bitmap)