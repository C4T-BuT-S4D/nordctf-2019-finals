from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP

cap = rdpcap('../task/bypass.pcapng.gz')
print('Done reading capture')

print(cap)

results = b''

for pkt in cap:
    if DNS in pkt and IP in pkt:
        # print(pkt)
        dst = pkt[IP].dst
        if dst == '104.196.158.159':
            if pkt.qdcount > 0 and isinstance(pkt.qd, DNSQR):
                name = pkt.qd.qname
                if name:
                    results += b''.fromhex(name.split(b'.')[0].decode())
            # results += bytes(raw_data)

print(results)

# print(f'Got flag data: {decode(results)}')
