import socket
import sys
import binascii
from JsonTraductor import *
from random import randint
import _thread

class Servidor:
    #host="192.168.0.40"
    #UDP_IP=host
    #UDP_PORT=10000

    tarjetas = [["F4", "FE", "AB", "56"],
                   ["04", "2D", "7F", "56"],
                   ["14", "88", "1B", "00"]]


    def __init__(self,UDP_IP,UDP_PORT):
        print("Servido wipy")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((UDP_IP,UDP_PORT))
        self.sock.listen(1)

    def conectar(self):
        print("True o False para Habilitar o deshabilitar" )
        while True:
                print ("Esperando conexión...")
                sc, addr = self.sock.accept()
                print ("Cliente conectado desde: ", addr)
                self.threadFunction(sc)
                print("terminado de crear el thread")                
                while True:
                        recibido = sc.recv(4098)
                        jsn=recibido.decode('utf-8')
                        print(jsn)
                        if 'tarjetaId' in jsn:
                            print("--ESTOY EN TARJETA--")
                            id=JsonTraductor.convertMensajeTarjeta(recibido)
                            print(id)
                            boo=self.validarTarjeta(id)
                            sc.send((JsonTraductor.convertValidaTarjeta(boo)).encode('utf-8'))
                            print("enviado")
                        elif 'sensor' in jsn:
                            print("--ESTOY EN SENSOR--")
                            sensorPaso=JsonTraductor.convertEstadoSensor(recibido)
                            print(sensorPaso)
                        elif 'habilitar' in jsn:
                            print("--ESTOY viendo si esta deshabilitado--")
                            habilitado=JsonTraductor.convertMensajeHabilitado(recibido)
                            print("habilitado?: ",habilitado)

        print ("Adios")
        sc.close()
        s.close()

    def threadFunction(self,sc):
        #resp=threading.Thread(self.enviarComando(sc))                        
        _thread.start_new_thread(self.enviarComando, (sc,))

    def enviarComando(self,sc):
        while True:
            enviar= str(input(""))
            print (enviar)
            msgEnvio=JsonTraductor.convertRespuestaServer(self.str2bool(enviar))
            sc.send(msgEnvio.encode('utf-8'))

    def str2bool(self,v):
        return v.lower() in ("yes", "true", "t", "1")

    def validarTarjeta(self,uid):
        ran=randint(0, 1)
        print("numero random",ran)
        if(ran==1):
            return True
        else:
            return False
