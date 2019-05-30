from machine import Pin,I2C
from SensorTarjeta.lib.automata import accepts_left, accepts_right
from SensorTarjeta.Sensor import *
from lopy4.lib.pyscan import Pyscan
from lopy4.lib.MFRC630 import MFRC630
from lopy4.NfcReader import *
from led.lib.pyb_i2c_lcd import I2cLcd
import pycom
import time


def main():
    pycom.heartbeat(False)
    print("ESTOY CORRIENDO")
    #10000 = 10 seg aprox
    sensor = Sensor("P17","P18",10000)
    nfcReader = NfcReader()
    i2c = I2C(1, I2C.MASTER, baudrate=100000,pins=('P20', 'P19'))
    print(i2c.scan())
    lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
    lcd.write_data("Apoye tarjeta")
    while True:
    ##    print(sensor.listen())
        lecturaNFC=nfcReader.discovery_loop()
        print(lecturaNFC)
        if(lecturaNFC==1):
            lcd.write_data("Tarjeta valida")
            lecturaSensor=sensor.listen()
            print("lectura del sensor: ", lecturaSensor)
            if(lecturaSensor==1):
                lcd.write_data("Entrada")
                time.sleep(3)
            if(lecturaSensor==2):
                lcd.write_data("Salida")
                time.sleep(3)
            if(lecturaSensor==0):
                lcd.write_data("time out")
                time.sleep(3)
            print("terminando de leer")
            time.sleep(3)
            lcd.write_data("Apoye tarjeta")
        if(lecturaNFC==2):
            lcd.write_data("Tarjeta invalida")
            time.sleep(3)
            lcd.write_data("Apoye tarjeta")

if __name__ == '__main__':
    main()
