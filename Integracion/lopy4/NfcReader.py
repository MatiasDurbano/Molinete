from .lib.pyscan import Pyscan
from .lib.MFRC630 import MFRC630
from .lib.LIS2HH12 import LIS2HH12
from .lib.LTR329ALS01 import LTR329ALS01
import binascii
import time
import pycom
import _thread
import struct

class NfcReader:
    #Reemplazar por  datos de bd
    VALID_CARDS = [[0xF4, 0xFE, 0xAB, 0x56],
                   [0x04, 0x2D, 0x7F, 0x56],
                   [0x14, 0x88, 0x1B, 0x00]]

    #defino colores para ver si la tarjeta es valida o no
    RGB_BRIGHTNESS = 0x8
    RGB_RED = (RGB_BRIGHTNESS << 16) # invalida
    RGB_GREEN = (RGB_BRIGHTNESS << 8) #valida
    RGB_BLUE = (RGB_BRIGHTNESS) #color predeterminado

    enable=True

    def __init__(self):
        self.py = Pyscan()
        self.nfc = MFRC630(self.py)
        self.nfc.mfrc630_cmd_init()

    def check_card(self,uid,len):
        return self.VALID_CARDS.count(uid[:len])

    def discovery_loop(self):
        print("el estado del nfc es: ",self.enable)
        if self.enable is True:
            atqa = self.nfc.mfrc630_iso14443a_WUPA_REQA(self.nfc.MFRC630_ISO14443_CMD_REQA)
            if (atqa != 0):
                    # A card has been detected, read UID
                uid = bytearray(10)
                uid_len = self.nfc.mfrc630_iso14443a_select(uid)
                print(self.nfc.format_block(uid, uid_len))
                if (uid_len > 0):
                    print(uid)
                        #aca deberia fijarme si la tarjeta es una de las que esta en la bd
                    return self.nfc.format_block(uid, uid_len)

    def setEnable(self, enable):
        self.enable=enable
        print("habilitado: ",self.enable)
