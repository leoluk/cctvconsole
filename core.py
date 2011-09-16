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

import socket
import keymap

getTemplateByByte = lambda x: ('''\xff\xff\xff\xff\x00\x00\x00\x00\x00\x01\x10\xc0\x11\x00\x00\x00'''
                               +chr(x)+'''\x00\x00\x00\x00\x00\x00\x00xV4\x12''' + '\x00'*996)

def getTemplateByName(name):
    return getTemplateByByte(keymap.getKeyByte(name))

class ControlSocket(socket.socket):
    def __init__(self, host, port):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port,))

    def sendKeyByte(self, byte):
        self.send(getTemplateByByte(byte))
        self.send(getTemplateByName("C_ACK"))

    def sendKey(self, name):
        self.sendKeyByte(keymap.getKeyByte(name))
