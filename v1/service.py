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
        self._player_percentage = 0

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
            logging.error("Host is not found or kodi is not started")
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

    @property
    def playerPercentage(self):
        return self._player_percentage
    @playerPercentage.setter
    def playerPercentage (self, val):
        if not self._player_percentage == val :
            if val == self._player_percentage +1 or val == self._player_percentage +2:
                self._player_percentage = val
            else :
                logging.debug("%s -> %s",self._player_percentage,val)
                self._player_percentage = val+2
                self.uploader("0:0:"+str(self._player_percentage))
    
    def musicPlayer(self):
        jsplayerprogress = self.jstemp
        jsplayerprogress["method"] = "Player.GetProperties"
        jsplayerprogress["id"] = "player_percentage"
        jsplayerprogress["params"] = {
            "playerid":0,
            "properties":["percentage"]
        }
        self.playerPercentage = int(requests.post(self.Host, json=jsplayerprogress).json()['result']['percentage'])

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
        m.artist = self.charLimiter(result['artist'][0],20)
        m.album = self.charLimiter(result['album'],20)
        m.genre = result['genre'][0]
        m.year = str(result['year'])
        m.duration = str(result['duration'])
        _mtitle = self.charLimiter(result['title'],60) # fix uploding loop 
        if not m.title == _mtitle :
            m.title = _mtitle
            message = "0:1:"+m.track+":"+m.title
            self.uploader(message)
            message = "0:2:"+m.artist+":"+m.album+":"+m.genre+":"+m.year+":"+m.duration
            self.uploader(message)

    def charLimiter(self, string, length_limit):
        ch_list = list(string)
        if len(ch_list) >= length_limit :
            ch_res = ''.join(ch_list[0:length_limit])
            return ch_res
        else :
            return string

    def uploader(self, message):
        logging.debug("uploader(%s) = %s",len(message),message)
        if len(message) >65 :
            logging.warning("The message length is excesses %s",len(message))
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
        v.videoType = result["type"]
        v.showTitle = result["showtitle"]
        v.season = str(result["season"])
        v.episode = str(result["episode"])
        v.votes = str(result["votes"])
        if not v.title == result['title'] :
            v.title = result["title"]
            message = str(1)+":"+v.videoType+":"+v.showTitle+":"+v.season+":"+v.episode+":"+v.votes
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
        