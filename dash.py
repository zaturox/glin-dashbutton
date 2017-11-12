#!/usr/bin/env python3

import argparse
import socket
import struct
import zmq

argparser = argparse.ArgumentParser(
        description = "Use Amazon DASH-Button for glin")
argparser.add_argument("dash_mac", help = 'MAC-address of DASH-Button, in lowercase and with colon, eg. "01:23:45:67:89:ab"')
argparser.add_argument("zmq_target", help = 'ZeroMQ-address of glin, eg "tcp://127.0.0.1:6607"')
argparser.add_argument("-i", "--interface", help = "Interface to listen. If not given, listen all.")
args = argparser.parse_args()

dash_mac = int(args.dash_mac.replace(':', '').replace('-',''), 16)


def isDashInit(packet):
    (dstmac, srcmac, ethertype) = tuple(map(lambda x: int.from_bytes(x, byteorder="big", signed=False), struct.unpack("!6s6s2s", packet[0][0:14])))
    if ethertype == 0x0806:
        if srcmac == dash_mac and dstmac == 0xffffffffffff:
            if struct.unpack("2s2s1s1s2s6s4s6s4s", packet[0][14:42])[4] == b"\x00\x01":
                return True
    return False

def toggle_mainswitch():
    pusher.send(b"mainswitch.toggle")

def isArp(packet):
    pass

ctx = zmq.Context()
pusher = ctx.socket(zmq.PUSH)
pusher.connect(args.zmq_target)


rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
if args.interface:
    rawSocket.bind((args.interface,0))

try:
    while True:
        packet = rawSocket.recvfrom(2048)
        if isDashInit(packet):
            toggle_mainswitch()
            print("Dash pressed!")
except KeyboardInterrupt:
    pass
