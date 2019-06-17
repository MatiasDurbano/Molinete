from lib.Servidor import *
#from lib.Wifi import *

def main():
    #wifi = Wifi("HITRON-92B0","VALUP3MCSRD3")
    #wifi = Wifi("TG1672G62","becarios")
    #wifi.connect()
    #print("esta conectado: ",wifi.isconnected())
    server=Servidor("0.0.0.0",10000)
    server.conectar()


if __name__ == '__main__':
    main()
