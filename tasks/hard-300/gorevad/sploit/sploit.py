from Crypto.Cipher import AES
from scapy.all import *
from scapy.layers.inet import IP, TCP

cap = rdpcap('../task/traffic.pcapng.gz')
print('Done reading capture')

print(cap)

state_key = None


def unpad(s):
    return s[:-s[-1]]


need_size = 0
current_data = b''

for pkt in cap:
    if TCP in pkt and pkt[IP].dst == '10.40.0.23' and len(pkt[TCP].payload):
        payload = bytes(pkt[TCP].payload)
        print(f'Payload: {payload}')

        if len(current_data) < need_size:
            current_data += payload[4:]
        else:
            pkt_size, = struct.unpack("<I", payload[:4])
            print(f'Size: {pkt_size}')
            need_size = pkt_size
            current_data = payload[4:]

        if len(current_data) < need_size:
            continue

        pkt_size = need_size
        if pkt_size == 16:
            state_key = payload[4:]
            continue

        iv = payload[-16:]
        data = payload[4:-16]
        aes = AES.new(state_key, AES.MODE_CBC, iv)
        decrypted = unpad(aes.decrypt(data))
        print(f'Got decrypted data: {decrypted}')
        # break
