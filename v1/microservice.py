import serial
import logging
import time

class Arduino:
    def __init__(self,port="COM3",baudrate=9600,rtscts=True,dsrdtr=True):
        self._isConeected = False
        self._port = port
        self._baudrate = baudrate
        self._delay = 2
        try :
            self.s = serial.Serial(port=self._port,baudrate=self._baudrate)
            logging.debug("preparing serial communication")
            time.sleep(1.5)
        except :
            logging.error("serial not found")

    def send(self,msg):
        self.s.flush()
        # logging.debug("sending %s",msg)
        self.s.write(msg.encode())
        logging.debug("please wait...(%ss)",self._delay)
        '''
        delay is needed for arduino process. the optimal is 2 seconds
        '''
        time.sleep(self._delay)

        
'''bug
0:3:Winter (Basse Dance):Blackmore's Night:Winter Carols:2006:187 Error duration 00:01 =>66 char
0:9:Wish You Were Here:Blackmore's Night:Winter Carols:2006:302 OK =>65
max is 65 char
'''
