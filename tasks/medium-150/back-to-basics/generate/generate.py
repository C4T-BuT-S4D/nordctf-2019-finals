import random
import time

from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
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
                   '(': '-.--.', ')': '-.--.-', ' ': ' '}


def send_icmp_packet(ip, payload):
    pkt = IP(dst=ip) / ICMP() / payload
    p = sr1(pkt)
    return p


def encode_char(c):
    c = c.upper()
    if c in MORSE_CODE_DICT or c == ' ':
        return c
    if c == '{':
        code = 'openingcurlybrace'
    elif c == '}':
        code = 'closingcurlybrace'
    else:
        assert False

    return ''.join(map(encode_char, code))


def encode(s):
    formatted = '.'.join(encode_char(ch) for ch in s)
    morse = ' '.join(MORSE_CODE_DICT[ch] for ch in formatted)
    return morse.replace('.', '0').replace('-', '1')


flag = 'flagislowercaseflag{46db0a4b678114cd2fbc25df77111640}'

encoded = encode(flag)
print(encoded)
print(len(encoded))

blocks = [encoded[i:i + 5] for i in range(0, len(encoded), 5)]
# chars = ''.join(chr(int(x, 2)) for x in blocks)
# print(chars)

# for c in chars:
#     print(repr(send_icmp_packet('10.40.0.23', c)))

for i, block in enumerate(blocks):
    send_icmp_packet('10.40.0.23', ''.join(block))
    time.sleep(random.random() * 2)
    print(f'Done block {i + 1} of {len(blocks)}')

print('Done!')
