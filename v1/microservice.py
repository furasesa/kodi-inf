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
            time.sleep(2)
            self._isConeected = True
        except :
            logging.error("serial not found")
            

    def send(self,msg):
        if self._isConeected :
            self.s.flush()
            time.sleep(.5)
            # logging.debug("sending %s",msg)
            self.s.write(msg.encode())
            logging.debug("please wait...(%ss)",self._delay)
            '''
            delay is needed for arduino process. the optimal is 2 seconds
            '''
            time.sleep(self._delay)
        pass

        
'''bug
0:3:Winter (Basse Dance):Blackmore's Night:Winter Carols:2006:187 Error duration 00:01 =>66 char
0:9:Wish You Were Here:Blackmore's Night:Winter Carols:2006:302 OK =>65
max is 65 char
vtype = 1
track_num = 2
title = 20
artist = 15
album = 15
year = 4
duration = 3
spearator char = 6
'''
