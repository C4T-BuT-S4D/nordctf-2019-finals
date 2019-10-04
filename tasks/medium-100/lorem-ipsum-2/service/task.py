#!/usr/bin/env python2

import random
import loremipsum

from subprocess import Popen, PIPE


def main():
    length = random.randint(16, 32)
    paragraphs = loremipsum.get_paragraphs(length, True)
    text = '\n\n'.join(paragraphs)
    process = Popen(['stegsnow', '-C', '-f', 'flag.txt'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(text)
    print(stdout.strip())


if __name__ == '__main__':
    main()
