import threading
import queue
import requests
import logging
import time
from microservice import Arduino
import musicProperty as m
import videoProperty as v

# q=queue.Queue()

class Kodi:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', )

    def __init__(self,url="localhost:8080",arduino=None):
        self.jstemp = {"jsonrpc" : "2.0"}
        self.arduino = arduino
        self._host = "http://"+url+"/jsonrpc"
        self._isconnected = False
        self._playerid = None
        self._delay = 1

    @property
    def Host(self):
        return self._host
    @Host.setter
    def Host(self,val):
        if not self._host == val :
            self._host = "http://"+val+"/jsonrpc"
            logging.debug("Host change to %s",self._host)
            # self.isConnected
    @property
    def isConnected(self):
        try:
            ping = self.jstemp
            ping["method"] = "JSONRPC.Ping"
            ping["id"] = "ping"
            requests.post(self.Host, json=ping).json()['result']
            return True
        except:
            return False
    @isConnected.setter
    def isConnected(self,val):
        self._isconnected=val

    @property
    def playerId(self):
        return self._playerid
    @playerId.setter
    def playerId(self,val):
        self._playerid = val
        while val == 0 or val == 1:
            if val == 0:
                self.musicPlayer()
                time.sleep(self._delay)
            elif val == 1:
                self.videoPlayer()
                time.sleep(self._delay)
            else :
                logging.error("Other Player ID")

    
    def musicPlayer(self):
        mplayer = self.jstemp
        mplayer["method"] = "Player.GetItem"
        mplayer["id"] = "mplayer"
        mplayer["params"]= {
            "playerid":0,
            "properties":["title","artist","genre","year","album","track","duration"]
        }
        result = requests.post(self.Host, json=mplayer).json()['result']['item']
        # logging.debug(result)
        m.track = str(result['track'])
        m.artist = result['artist'][0]
        m.album = result['album']
        m.genre = result['genre'][0]
        m.year = str(result['year'])
        m.duration = str(result['duration'])
        if not m.title == result['title'] :
            m.title = result['title']
            message = str(0)+":"+m.track+":"+m.title+":"+m.artist+":"+m.album+":"+m.year+":"+m.duration
            self.uploader(message)

    def uploader(self, message):
        logging.debug("uploader : %s",message)
        self.arduino.send(message)

    def videoPlayer(self):
        vplayer = self.jstemp
        vplayer["method"] = "Player.GetItem"
        vplayer["id"] = "vplayer"
        vplayer["params"]= {
            "playerid":1,
            "properties":["showtitle", "title","season","episode","votes"]
        }
        result = requests.post(self.Host, json=vplayer).json()['result']['item']
        
        v.showTitle = result["showtitle"]
        v.videoType = result["type"]
        v.season = str(result["season"])
        v.episode = str(result["episode"])
        v.votes = str(result["votes"])
        if not v.title == result['title'] :
            v.title = result["title"]
            # message = str(1)+

        # logging.debug("\nshowtitle\t:%s\nseason\t\t:%s\nepisode\t\t:%s\ntitle\t\t:%s\nvotes\t\t:%s",showtitle,season,episode,title,votes)

    def run(self):
        while self.isConnected:
            jsplayerid = self.jstemp
            jsplayerid["method"] = "Player.GetActivePlayers"
            jsplayerid["id"] = "playerid"
            self.playerId = requests.post(self.Host, json=jsplayerid).json()['result'][0]['playerid']
            time.sleep(self._delay)



        

      

a = Arduino()
k = Kodi(arduino=a)

# k.Host = "localhost:8080"
k.run()
        