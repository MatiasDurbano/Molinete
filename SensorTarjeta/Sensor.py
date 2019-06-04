from machine import Pin
from lib.automata import accepts_left, accepts_right
import pycom
import time

class Sensor():

    def __init__(self,PinRight, PinLeft):
        self.right_sensor = Pin(PinRight, mode=Pin.IN, pull=Pin.PULL_UP)
        self.left_sensor = Pin(PinLeft, mode=Pin.IN, pull=Pin.PULL_UP)
        self.record_list = [] #Que pasa si se queda colgado agregando elementos a la lista?
        self.record_active = False
        self.waiting = 0

    def clear(self):
        self.record_list = [] #vacío lista
        self.waiting = 0 #El waiting terminó

    def listen(self):
        while True:
            #print(self.right_sensor(),self.left_sensor())
            tupla=(self.right_sensor(),self.left_sensor())
            if(tupla[0]!=0 or tupla[1]!=0):
                self.record_active = True #Empezar el record
                self.record_list.append(tupla)
                print("Se ha grabado una tupla: ", tupla)

            if (tupla[0] == 0 and tupla[1] == 0 and self.record_active is True):
                self.waiting += 1
            # se debe agregar un waiting para la transición de un sensor a otro
            if (tupla[0] == 0 and tupla[1] == 0 and self.record_active is True and self.waiting > 1000):
                print(self.waiting)
                print("Ahora la bandera es False")
                self.record_active = False #Parar el record
                if (accepts_left(self.record_list)): #analizar el automata
                    print("entre en accept left")
                    print("izquierda a derecha")
                    pycom.rgbled(0x00ff00)
                    time.sleep(10)
                    self.clear()
                    return 0

                if (accepts_right(self.record_list)):
                    print("entre en accept right")
                    print("derecha a izquierda")
                    pycom.rgbled(0xff0000)
                    time.sleep(10)
                    self.clear()
                    return 1

                self.clear()
