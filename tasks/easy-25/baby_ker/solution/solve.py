import json
from Crypto.Util.number import long_to_bytes

with open("task.txt", "r") as f:
    s = f.read()

task = json.loads(s)

n = task["n"]
c = task["c"]

m = pow(c, 2, n)

print(long_to_bytes(m).decode())