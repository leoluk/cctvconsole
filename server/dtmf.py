#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright (c) 2011 Leopold Schabel
#   All rights reserved.
#
#   This copyright notice MUST APPEAR in all copies of the script!
#   In case of abuse or illegal redistribution please contact me:
#   mail@leoschabel.de
#


import audiere

KEYS = ('1', '2', '3', 'A',
        '4', '5', '6', 'B',
        '7', '8', '9', 'C',
        '*', '0', '#', 'D')

F1 = [697, 770, 852, 941]
F2 = [1209, 1336, 1477, 1633]

def get_frequencies(symbol):
    index = KEYS.index(symbol)
    return F1[index/4], F2[index%4]

def outstreams(self, symbol):
    f1, f2 = get_frequencies(symbol)
    return self.create_tone(f1), self.create_tone(f2)

def main():
    pass

if __name__ == '__main__':
    main()