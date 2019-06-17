import network
import machine
from network import WLAN
import time
#
# Set up WLAN
#
class Wifi:
    #ssid     = 'HITRON-92B0'
    #password = 'VALUP3MCSRD3'
    #ip       = '192.168.0.40'
    #net_mask = '225.225.225'
    #gateway  = '192.168.0.1'
    #dns      = 'hitronhub.home'
    wlan = WLAN(mode=WLAN.STA) # get current object, without changing the mode

    def __init__(self,ssid,key):
        self.ssid=ssid
        self.key=key

    def connect(self):
        nets = self.wlan.scan()
        for net in nets:
            if net.ssid == self.ssid:
                print('Network found!')
                self.wlan.connect(net.ssid, auth=(net.sec, self.key), timeout=500)
                while not self.wlan.isconnected():
                    machine.idle() # save power while waiting
                print('WLAN connection succeeded!')
                print(self.wlan.ifconfig())
                break
    def isconnected(self):
        return self.wlan.isconnected()

    def set(self):
        if not wlan.isconnected():
            connect(self)
#set()
#
# Set up server
#
#print("ejecutado")
