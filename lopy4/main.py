from lib.pyscan import Pyscan
from lib.MFRC630 import MFRC630
import _thread
import time
from NfcReader import *

def main():
  nfcReader = NfcReader()
  while True:
      print(nfcReader.discovery_loop())
      time.sleep(1)


if __name__ == '__main__':
    main()
