from NfcReader import *

def main():
    pycom.heartbeat(False)
    nfcReader = NfcReader()
    nfcReader.discovery_loop()

if __name__ == '__main__':
    main()
