from machine import Pin,I2C
from SensorTarjeta.lib.automata import accepts_left, accepts_right
from SensorTarjeta.Sensor import *
from lopy4.lib.pyscan import Pyscan
from lopy4.lib.MFRC630 import MFRC630
from lopy4.NfcReader import *
from led.lib.pyb_i2c_lcd import I2cLcd
from Red.Cliente import *
from Red.Wifi import *
from Red.JsonTraductor import *
import _thread
import pycom
import time


wifi = Wifi("HITRON-92B0","VALUP3MCSRD3")
wifi.connect()
cliente= Cliente("192.168.0.15",10000)
sensor = Sensor("P17","P18",10000)
nfcReader = NfcReader()
sensor = Sensor("P17","P18",10000)
i2c = I2C(1, I2C.MASTER, baudrate=100000,pins=('P20', 'P19'))
print(i2c.scan())
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
lcd.write_data("Apoye tarjeta")

def main():
    pycom.heartbeat(False)
    print("ESTOY CORRIENDO")
    print("esta conectado: ",wifi.isconnected())
    _thread.start_new_thread(lister, ())
    while True:
    ##    print(sensor.listen())
        #print("habilitar")
        lecturaNFC=nfcReader.discovery_loop()
        if not lecturaNFC is None:
            respuesta=cliente.sendMessage(JsonTraductor.convertJsonTarjeta(lecturaNFC))
            print("respuesta tarjeta ",respuesta)
            if(JsonTraductor.convertRespuestaTarjeta(respuesta)==True):
                lcd.write_data("Tarjeta valida")
                lecturaSensor=sensor.listen()
                print("lectura del sensor: ", lecturaSensor)
                if(lecturaSensor==1):
                    cliente.sendUnansweredMessage(JsonTraductor.convertJsonSensor("entrada"))
                    lcd.write_data("Entrada")
                    time.sleep(1)
                    pycom.rgbled(0x000000)
                if(lecturaSensor==2):
                    cliente.sendUnansweredMessage(JsonTraductor.convertJsonSensor("salida"))
                    lcd.write_data("Salida")
                    time.sleep(2)
                    pycom.rgbled(0x000000)
                if(lecturaSensor==0):
                    cliente.sendUnansweredMessage(JsonTraductor.convertJsonSensor("time out"))
                    lcd.write_data("time out")
                    time.sleep(2)
                print("terminando de leer")
                time.sleep(2)
                lcd.write_data("Apoye tarjeta")
            else:
                lcd.write_data("Tarjeta invalida")
                time.sleep(1)
                lcd.write_data("Apoye tarjeta")

def lister():
    while True:
        msgServer=cliente.ServerLister()
        print("thread respuesta: ",msgServer)
        resp=JsonTraductor.convertMensajeServer(msgServer)
        if not resp is None:
            print("habilito?: ",resp)
            nfcReader.setEnable(resp)
            cliente.clearData()
            cliente.sendUnansweredMessage((JsonTraductor.convertRespuestaServer(resp)).encode('utf-8'))
            if resp is False:
                lcd.write_data("Deshabilitado")
            else:
                lcd.write_data("Apoye tarjeta")



if __name__ == '__main__':
    main()
