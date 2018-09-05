import threading
import logging
import requests
import json
import time
import sys

class Extract(dict):
    class NADict(object):
        def __getitem__(self, k):
            return "N/A"
    NA = NADict()
    def __missing__(self, k):
        return self.NA

class MyKodi(threading.Thread):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )
    def __init__(self, host="localhost:8080", username="kodi", password="kodi") :
        threading.Thread.__init__(self, name="MAIN")

        self._player_type = None
        self._player_label = None
        self._host = host
        self._username = username
        self._password = password
        
        # self._is_connected = threading.Condition()

    @property
    def isConnected(self):
        return self._is_connected
    @isConnected.setter
    def isConnected(self, val):
        self._is_connected = val
    @property
    def username (self):
        return self._username
    @username.setter
    def username (self,val):
        self._username = val
        logging.debug("set username to %s",self._username)
    @property
    def password (self):
        return self._password
    @password.setter
    def password (self,val):
        self._password = val
        logging.debug("set password to %s",self._password)
    @property
    def host(self):
        return self._host
    @host.setter
    def host(self,val):
        self._host = "http://"+val+"/jsonrpc"
        logging.debug("changing host to %s",self._host)
        MyKodi.Connection().start()
        # MyKodi.checker(self)

    @property
    def playerType(self):
        return self._player_type
    @playerType.setter
    def playerType(self, val):
        self._player_type = val

    @property
    def playerLabel(self):
        # logging.info("Player Label : %s", self._player_label)
        return self._player_label

    @playerLabel.setter
    def playerLabel(self, val) :
        self._player_label = val

    def checker (self):
        ping = {
                "jsonrpc" : "2.0",
                "method" : "JSONRPC.Ping",
                "id" : "ping"
            }
        # logging.debug("connecting to %s with username %s pass %s",self._host,self._username,self._password)
        try :
            known_host = Extract(requests.post(self._host, json=ping, auth=(self._username,self._password)).json())['result']
            if known_host=='pong':
                logging.info("connection OK")
        except:
            logging.error("%s is unknown",self._host)
        finally :
            self._is_connected = True

    def run(self) :
        trial_error = 0
        trial_success = 0
        delay = 0.5
        # com1 = Comparation()
        # com2 = Comparation()
        # while self._is_connected :
        logging.debug("running")


        # while True :
        #     with self._condition :
        #         self._condition.wait()
        #         # use private json name
        #         player = {
        #             "jsonrpc" : "2.0",
        #             "id" : "playerinf",
        #             "method" : "Player.GetActivePlayers"
        #         }
        #         # logging.debug("sending : %s to %s", player, host)
        #         # player_id[0] = "dummy"
        #         try :
        #             trial_success += 1
        #             trial_error = 0
        #             player_id = Extract(requests.post(host, headers=header, json=player).json())['result'][0]['playerid']
        #             try :
        #                 player["method"]="Player.GetItem"
        #                 player["params"]={"playerid":player_id}
        #                 player_extract = Extract(requests.post(host, headers=header, json=player).json())['result']['item']
        #                 self.playerType = Extract(player_extract)['type']
        #                 self.playerLabel = Extract(player_extract)['label']
        #                 # com1[0] == self.playerType
        #                 # com2[0] = self.playerLabel
        #                 if not com2[0]:
        #                     # logging.debug("%s : %s",com1[0],com2[0])
        #                     logging.debug("%s : %s",self.playerType, self.playerLabel)
                        
        #                 time.sleep(delay)
        #             except :
        #                 logging.error("error gathering player information")
        #         except :
        #             trial_error += 1
        #             trial_success = 0
        #             if trial_error >= 5 :
        #                 break
        #             logging.debug("no active player")
    
    class Connection(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self,name="Connection")
            # self._host = host
            # self._username = username
            # self._password = password
        def run(self):
            logging.debug("running Host %s",self._host)
            ping = {
                "jsonrpc" : "2.0",
                "method" : "JSONRPC.Ping",
                "id" : "ping"
            }
            # logging.debug("connecting to %s with username %s pass %s",self._host,self._username,self._password)
            try :
                known_host = Extract(requests.post(self._host, json=ping, auth=(self._username,self._password)).json())['result']
                if known_host=='pong':
                    logging.info("connection OK")
            except:
                logging.error("%s is unknown",self._host)
            finally :
                self._is_connected = True

        
