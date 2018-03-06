#!/usr/bin/env python

import operator as op
import sys

static_bytes = [0x67, 0x39, 0x66, 0x2e, 0x46, 0x03, 0x51, 0x76]


def main():
    i = 0
    password = ''
    for e in static_bytes:
        res = op.xor(e, i)
        password += unichr(res)
        i += 0xa
    print(password)


if __name__ == '__main__':
    main()
    sys.exit(0)
