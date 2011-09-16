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


import os
import sys
import socket
import ConfigParser
import Queue
import threading
import time

import bottle
import audiere

import dtmf


if not "frozen" in dir(sys):
    sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))

import core
from bottle import route, view, request

socket.setdefaulttimeout(0.5)

parser = ConfigParser.ConfigParser(dict(remote_ip='192.168.1.254', remote_port='1024', debug='0', server_port='8080'))
parser.read("settings.ini")

if not parser.has_section("Server"):
    parser.add_section("Server")

bottle.debug(parser.getboolean('Server', 'debug'))

REMOTE = (parser.get('Server', 'remote_ip'),
          parser.getint('Server', 'remote_port'))

MAPPING = {
    'up': 'M_UP',
    'down': 'M_DOWN',
    'left': 'M_LEFT',
    'right': 'M_RIGHT',
    'cam1': 'N_1',
    'cam2': 'N_2',
    'cam3': 'N_3',
    'cam4': 'N_4',
    'iris_p': 'Z_IRIS_PLUS',
    'iris_m': 'Z_IRIS_MINUS',
    'zoom_p': 'Z_ZOOM_PLUS',
    'zoom_m': 'Z_ZOOM_MINUS',
    'focus_p': 'Z_FOCUS_PLUS',
    'focus_m': 'Z_FOCUS_MINUS',
    'cancel': 'F_ESC',
    'menu': 'F_MENU',
    'enter': 'F_ENTER',
    'display': 'F_DISPLAY',
   # 'list': 'F_LIST',
   # 'freeze': 'F_FREEZE',
    'set': 'F_SET',
    'hud': 'F_2',
   # 'help': 'F_1',
    'setpreset': 'F_SET_PRESET',
    'preset': 'F_GOTO_PRESET',
}

DTMFMAPPING = {
    'up': '2',
    'left': '4',
    'right': '6',
    'down': '8',
    'zoom_p': 'A',
    'zoom_m': 'B',
    'focus_p': 'C',
    'focus_m': 'D',
}

@route("/")
@view('control.html')
def main_route():
    return {}

class DTMFThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.device = audiere.open_device()

    def run(self):
        while True:
            symbol = self.queue.get()
            tones = dtmf.outstreams(self.device, symbol)
            for tone in tones: tone.play()
            time.sleep(0.5)
            for tone in tones: tone.stop()


class ControlThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            try:
                control = core.ControlSocket(*REMOTE)
                while True:
                    cmd = self.queue.get()
                    control.sendKey(cmd)
            except socket.error:
                print "CamServer socket crashed, reconnecting..."


queue = Queue.Queue()
control = ControlThread(queue)
control.start()

dtmfqueue = Queue.Queue()
dtmfcontrol = DTMFThread(dtmfqueue)
dtmfcontrol.start()

@route("/control")
def control_route():
    try:
        cmd = request.GET["cmd"]

        if not cmd.startswith("dtmf-"):
            queue.put(MAPPING[cmd])
        else:
            dtmfqueue.put(DTMFMAPPING[cmd.lstrip('dtmf-')])

    except KeyError:
        bottle.abort(400, "Invalid command.")

@route("/static/:path#.+#")
def static_route(path):
    return bottle.static_file(path, root=os.path.join(os.path.dirname(sys.argv[0]), 'static'), download=None)

bottle.TEMPLATE_PATH = os.path.dirname(sys.argv[0])
bottle.run(reloader=bottle.DEBUG, port=parser.getint('Server', 'server_port'), server="paste", host="0.0.0.0")
