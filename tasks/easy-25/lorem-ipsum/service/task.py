#!/usr/bin/env python2

import loremipsum


def main(flag):
    paragraphs = loremipsum.get_paragraphs(len(flag) + 1)
    print('\n\n'.join('%s\r%s' % pair for pair in zip(flag, paragraphs)))


if __name__ == '__main__':
    with open('flag.txt', 'r') as file:
        flag = file.read()
    main(flag)
