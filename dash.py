import argparse

argparser = argparse.ArgumentParser(
        description = "Use Amazon DASH-Button for glin")
argparser.add_argument("dash_mac", help = 'MAC-address of DASH-Button, in lowercase and with colon, eg. "01:23:45:67:89:ab"')
argparser.add_argument("zmq_target", help = 'ZeroMQ-address of glin, eg "tcp://127.0.0.1:6607"')
args = argparser.parse_args()

import scapy.all as spy
import zmq

def dash_received(packet):
    if (packet[spy.ARP].op == 1 and packet[spy.ARP].hwsrc == args.dash_mac and packet[spy.ARP].hwdst == "00:00:00:00:00:00"):
        print("Dash was pressed!")
        toggle_mainswitch()

def toggle_mainswitch():
    pusher.send(b"mainswitch.toggle")

ctx = zmq.Context()
pusher = ctx.socket(zmq.PUSH)
pusher.connect(args.zmq_target)

spy.sniff(prn=dash_received, filter="arp", iface="wlan0")
