from scapy.all import *
from scapy.layers.inet import IP, ICMP

cap = rdpcap('../back_to_basics.pcapng.gz')
print('Done reading capture')

print(cap)

results = b''

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...',
    'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',
    'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-',
    'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--',
    'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ', ': '--..--', '.': '.-.-.-',
    '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': ' ',
}


def decode_string(s):
    s = s.replace('0', '.').replace('1', '-')
    blocks = filter(lambda x: x != '', s.split(' '))
    decode_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    return list(decode_dict.get(block, '?') for block in blocks)


def decode(data):
    data = data.decode()
    decoded = ''.join(decode_string(data)).replace('.', ' ')
    return decoded


for pkt in cap:
    if ICMP in pkt:
        dst = pkt[IP].dst
        if dst == '10.40.0.23':
            raw_data = pkt[Raw]
            # print(raw_data)
            results += bytes(raw_data)

print(results)

print(f'Got flag data: {decode(results)}')
