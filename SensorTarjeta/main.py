from machine import Pin
from lib.automata import accepts_left, accepts_right
import pycom
import time
from Sensor import *

def main():
    pycom.heartbeat(False)
    sensor = Sensor("P21","P22")
    print(sensor.listen())
    
if __name__ == '__main__':
    main()
