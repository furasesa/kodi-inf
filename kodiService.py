import threading
import logging
import requests
import json
import time
import sys

# from info import Information

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )

#global
condition = threading.Condition()
header = {
            'Content-Type': 'application/json',
            'User-Agent': 'python-kodi'
        }   

def producer(host,username,password):
    delay = 1
    trial_success = 0
    trial_error = 0 
    # connection = Information.Connection()
    while True:
        with condition:
            ping = {
                "jsonrpc" : "2.0",
                "method" : "JSONRPC.Ping",
                "id" : "ping"
            }
            try:
                known_host = Extract(requests.post(host, json=ping, auth=(username,password)).json())['result']
                if known_host=='pong':
                    trial_error = 0
                    trial_success += 1
                    condition.notifyAll()
                    if trial_success >= 5:
                        continue
                    # connection.IsConnected = True
                    logging.debug("Connection status %s",connection.IsConnected)

            except:
                trial_success = 0
                trial_error += 1
                if trial_error >= 5 :
                    # sys.exit(1)
                    trial_error = 0
                    # connection.IsConnected = False
                    logging.error("error connection to %s, triying (%s)",host,trial_error)
        time.sleep(delay)


def consumer(id, args, kwarg, filterResult):
    with condition :
        logging.debug("waiting host")
        # logging.debug("args %s, kwargs %s",args,kwarg)
        condition.wait()
        params = {}
        params["jsonrpc"]="2.0"
        params["id"]=id
        params["method"]=args
        if kwarg :
            params["params"]=kwarg
        logging.debug("sending : %s to %s", params, host)
        # try :
        result = Extract(requests.post(host, headers=header, json=params).json())['result']
        if filterResult:
            result = Extract(result)[filterResult]
        logging.debug('result : %s',result)
        return result
        # except :
        #     logging.debug("error params %s", params)

class Extract(dict):
    class NADict(object):
        def __getitem__(self, k):
            return "N/A"
    NA = NADict()
    def __missing__(self, k):
        return self.NA

class Host(threading.Thread):
    def __init__(self, url="localhost:8080", name="Server",  user="kodi", passwd="kodi"):
        threading.Thread.__init__(self, name="Server")
        global host, username, password
        host = "http://"+url+"/jsonrpc"
        username = user
        password = passwd

    def run (self):
        logging.debug("running host")
        producer(host,username,password)

class Kodi(threading.Thread):
    def __init__(self, name=None, args=(), kwargs=None, id=None, getresult=None):
        threading.Thread.__init__(self, name=None, args=(), kwargs=None)
        self._args = args
        self._kwargs = kwargs
        self._getresult = getresult
        if isinstance(id,int):
            self._id += 1
        else :
            self._id = id
    def run(self):
        logging.debug("running Kodi")
        consumer(self._id, self._args, self._kwargs, self._getresult)


class Comparation (object):
    def __init__(self):
        self._ov = [1]
        self._ov[0] = None
        self.bool = False

    def __getitem__(self,k):
        return self.bool

    def __setitem__(self, k, new_val):
        self._nv = new_val
        if not self._ov[0] == self._nv :
            print("changed from ",self._ov[0],"to",self._nv)
            self._ov[0] = self._nv
            self.bool = False
            return
        self.bool = True


class Player (threading.Thread):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )
    def __init__(self, name=None) :
        threading.Thread.__init__(self, name=name)
        self._player_type = None
        self._player_label = None

    @property
    def playerType(self):
        # logging.info("Player Type : %s", self._player_type)
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

    def run(self) :
        trial_error = 0
        trial_success = 0
        delay = 0.5
        com1 = Comparation()
        com2 = Comparation()
        while True :
            with condition :
                condition.wait()
                # use private json name
                player = {
                    "jsonrpc" : "2.0",
                    "id" : "playerinf",
                    "method" : "Player.GetActivePlayers"
                }
                # logging.debug("sending : %s to %s", player, host)
                # player_id[0] = "dummy"
                try :
                    trial_success += 1
                    trial_error = 0
                    player_id = Extract(requests.post(host, headers=header, json=player).json())['result'][0]['playerid']
                    try :
                        player["method"]="Player.GetItem"
                        player["params"]={"playerid":player_id}
                        player_extract = Extract(requests.post(host, headers=header, json=player).json())['result']['item']
                        self.playerType = Extract(player_extract)['type']
                        self.playerLabel = Extract(player_extract)['label']
                        com1[0] == self.playerType
                        com2[0] = self.playerLabel
                        if not com2[0]:
                            # logging.debug("%s : %s",com1[0],com2[0])
                            logging.debug("%s : %s",self.playerType, self.playerLabel)
                        
                        time.sleep(delay)
                    except :
                        logging.error("error gathering player information")
                except :
                    trial_error += 1
                    trial_success = 0
                    if trial_error >= 5 :
                        break
                    logging.debug("no active player")












# class Information(object):
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', )
#     class Connection (object):
#         def __init__ (self, is_connected=False):
#             self._is_connected = is_connected

#         @property
#         def IsConnected(self):
#             logging.info("connected? %s",self._is_connected)
#             return self._is_connected

#         @IsConnected.setter
#         def IsConnected(self,value):
#             self._is_connected = value

        

#     class PlayerInfo(object) :
#         def __init__ (self,player_type=None, player_label=None):
#             self._player_type = player_type
#             self._player_label = player_label

#         @property
#         def playerType(self):
#             logging.info("Player Type : %s", self._player_type)
#             return self._player_type
#         @playerType.setter
#         def playerType(self, val):
#             self._player_type = val

#         @property
#         def playerLabel(self):
#             logging.info("Player Label : %s", self._player_label)
#             return self._player_label

#         @playerLabel.setter
#         def playerLabel(self, val) :
#             self._player_label = val