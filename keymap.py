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

class InvalidKeyName(Exception): pass

KEY_MAPPING = {
    "C_ACK": 0x3E,
    "F_SET_PRESET": 0x18,
    "F_GOTO_PRESET": 0x19,
    "F_FREEZE": 0x1E,
    "F_SET": 0x1C,
    "F_LIST": 0x1D,
    "F_1": 0x23,
    "F_2": 0x24,
    "F_3": 0x25,
    "F_4": 0x26,
    "F_5": 0x27,
    "F_DISPLAY": 0x1A,
    "F_SEQ": 0x22,
    "F_MENU": 0x1B,
    "F_ENTER": 0x16,
    "F_ESC": 0x17,
    "F_PLUS": 0x15,
    "F_MINUS": 0x14,
    "F_PLAY": 0x2E,
    "F_RWD": 0x2B,
    "F_FWD": 0x2F,
    "Z_ZOOM_PLUS": 0x39,
    "Z_ZOOM_MINUS": 0x38,
    "Z_IRIS_PLUS": 0x3B,
    "Z_IRIS_MINUS": 0x3A,
    "Z_FOCUS_PLUS": 0x3D,
    "Z_FOCUS_MINUS": 0x3C,
    "F_KNOB": 0x4F,
    "F_KNOB_ACTION": 0x51,
    "M_DOWN": 0x11,
    "M_UP": 0x10,
    "M_LEFT": 0x13,
    "M_RIGHT": 0x12,
}

# Num keys can be accessed as N_1, N_2, N_3, ...

KEY_MAPPING += {("N_%d" % num): num-1 for num in range(1,17)}

KEY_MAPPING_INVERTED = dict((v,k) for k,v in KEY_MAPPING.items())

def getKeyName(byte):
    return KEY_MAPPING_INVERTED[byte]

def getKeyByte(name):
    return KEY_MAPPING[name]





