import serial
import logging
import time

class Arduino:
    def __init__(self,port="COM3",baudrate=9600,timeout=2):
        self._isConeected = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

    def send(self,msg):
        s = serial.Serial(port=self._port,baudrate=self._baudrate,timeout=self._timeout)
        logging.debug("please wait...(2s)")
        time.sleep(2)
        logging.debug("sending %s",msg)
        s.write(msg.encode())
        
