import threading
import queue
import requests
import logging
from microservice import Arduino

# q=queue.Queue()

class Kodi:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', )

    def __init__(self,url="localhost:8080",arduino=None):
        self.jstemp = {"jsonrpc" : "2.0"}
        self.arduino = arduino
        self._host = "http://"+url+"/jsonrpc"
        self._isconnected = False
        self._playerid = None
        

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
        if val == 0:
            self.musicPlayer()
        elif val == 1:
            self.videoPlayer()
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
        # playerType = result['type']
        track = str(result['track'])
        title = result['title']
        artist = result['artist'][0]
        album = result['album']
        duration = str(result['duration'])
        genre = result['genre'][0]
        year = str(result['year'])
        message = str(0)+":"+track+":"+title
        # print (message)
        self.arduino.send(message)
        
        # logging.debug("artis %s\talbum %s\ttitle %s",playerArtist,playerAlbum,playerTitle)

    def videoPlayer(self):
        vplayer = self.jstemp
        vplayer["method"] = "Player.GetItem"
        vplayer["id"] = "vplayer"
        vplayer["params"]= {
            "playerid":1,
            "properties":["showtitle", "title","season","episode","votes"]
        }
        result = requests.post(self.Host, json=vplayer).json()['result']['item']
        showtitle = result["showtitle"]
        ptype = result["type"]
        season = str(result["season"])
        episode = str(result["episode"])
        title = result["title"]
        votes = str(result["votes"])
        logging.debug("\nshowtitle\t:%s\nseason\t\t:%s\nepisode\t\t:%s\ntitle\t\t:%s\nvotes\t\t:%s",showtitle,season,episode,title,votes)

    def run(self):
        if self.isConnected:
            try:
                jsplayerid = self.jstemp
                jsplayerid["method"] = "Player.GetActivePlayers"
                jsplayerid["id"] = "playerid"
                self.playerId = requests.post(self.Host, json=jsplayerid).json()['result'][0]['playerid']
            except:
                logging.error("error getting player id")


        

      

a = Arduino()
k = Kodi(arduino=a)

# k.Host = "localhost:8080"
k.run()
        