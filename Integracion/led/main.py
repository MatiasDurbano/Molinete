import pycom
from machine import I2C
import time
from lib.lcd.pyb_i2c_lcd import I2cLcd

pycom.heartbeat(False)
i2c = I2C(0, I2C.MASTER, baudrate=100000)
print(i2c.scan()[0])

lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
#soporta hasta 32 caracteres por el momento
lcd.write_data("Hola todo mundo, escribo abajo")
