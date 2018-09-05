import threading
import logging
import requests
import json
import time
import sys
import serial

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )

#global
condition = threading.Condition()
header = {
            'Content-Type': 'application/json',
            'User-Agent': 'python-kodi'
        }
arduino_connected = False
try :
    arduino = serial.Serial("/dev/ttyACM0",115200,timeout=2)
    arduino_connected = True
    logging.debug("arduino connected")
    # waiting arduino LCD render
    time.sleep(2)
except :
    arduino_connected = False
    logging.error("arduino is not connected")


def producer(host,username,password):
    delay = 1
    trial_success = 0
    trial_error = 0 
    logging.debug("running producer")
    while True:
        with condition:
            # logging.debug("condition ok")
            ping = {
                "jsonrpc" : "2.0",
                "method" : "JSONRPC.Ping",
                "id" : "ping"
            }
            try:
                known_host = Extract(requests.post(host, json=ping).json())['result']
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

class Player (threading.Thread):
    def __init__(self, name=None) :
        threading.Thread.__init__(self, name=name)
        self._player_type = None
        self._player_label = None
        self._player_title = None
        self._player_artist = None
        self._player_albumartist = None
        self._player_genre = None
        self._player_year = None
        self._player_rating = None
        self._player_album = None
        self._player_track = None
        self._player_duration = None
        self.delay = 1 #requires for refresh rate LCD and baudrate transfer

    @property
    def playerType(self):
        return self._player_type

    @playerType.setter
    def playerType(self, val) :
        if not self._player_type == val:
            logging.debug("Type :%s", self.playerType)
            self._player_type = val
            playertype="ptype:"+self.playerType
            print(playertype)
            try :
                if arduino_connected :
                    arduino.write(playertype.encode())
            except :
                logging.error("Error sending PlayerType")

    @property
    def playerLabel(self):
        return self._player_label

    @playerLabel.setter
    def playerLabel(self, val) :
        if not self._player_label == val:
            logging.debug("Label :%s", self.playerLabel)
            self._player_label = val
            label="label:"+self.playerLabel
            print(label)
            try :
                if arduino_connected :
                    arduino.write(label.encode())
            except :
                logging.error("Error sending Label")

    @property
    def playerTitle(self):
        return self._player_title

    @playerTitle.setter
    def playerTitle(self, val) :
        if not self._player_title == val:
            logging.debug("Title :%s", self.playerTitle)
            self._player_title = val
            title="title:"+self.playerTitle
            print(title)
            try :
                if arduino_connected :
                    arduino.write(title.encode())
                    time.sleep(self.delay)
            except :
                logging.error("Error sending Title")

    @property
    def playerArtist(self):
        return self._player_artist

    @playerArtist.setter
    def playerArtist(self, val) :
        if not self._player_artist == val:
            logging.debug("Artist :%s", self.playerArtist)
            self._player_artist = val
            artist="artist:"+self.playerArtist
            print(artist)
            try :
                if arduino_connected :
                    arduino.write(artist.encode())
            except :
                logging.error("Error sending Artist")

    @property
    def playerAlbumArtist(self):
        return self._player_albumartist

    @playerAlbumArtist.setter
    def playerAlbumArtist(self, val) :
        if not self._player_albumartist == val:
            logging.debug("AlbumArtist :%s", self.playerAlbumArtist)
            self._player_albumartist = val
            albumartist="albumartist:"+self.playerAlbumArtist
            print(albumartist)
            try :
                if arduino_connected :
                    arduino.write(albumartist.encode())
            except :
                logging.error("Error sending AlbumArtist")

    @property
    def playerGenre(self):
        return self._player_genre

    @playerGenre.setter
    def playerGenre(self, val) :
        if not self._player_genre == val:
            logging.debug("Genre :%s", self.playerGenre)
            self._player_genre = val
            genre="genre:"+self.playerGenre
            print(genre)
            try :
                if arduino_connected :
                    arduino.write(genre.encode())
            except :
                logging.error("Error sending Genre")

    @property
    def playerYear(self):
        return self._player_year

    @playerYear.setter
    def playerYear(self, val) :
        if not self._player_year == val:
            logging.debug("Year :%s", self.playerYear)
            self._player_year = val
            year="year:"+self.playerYear
            print(year)
            try :
                if arduino_connected :
                    arduino.write(year.encode())
            except :
                logging.error("Error sending Year")

    @property
    def playerAlbum(self):
        return self._player_album

    @playerAlbum.setter
    def playerAlbum(self, val) :
        if not self._player_album == val:
            logging.debug("Album :%s", self.playerAlbum)
            self._player_album = val
            album="album:"+self.playerAlbum
            print(album)
            try :
                if arduino_connected :
                    arduino.write(album.encode())
            except :
                logging.error("Error sending Album")


    @property
    def playerTrack(self):
        return self._player_track

    @playerTrack.setter
    def playerTrack(self, val) :
        if not self._player_track == val:
            logging.debug("Track :%s", self.playerTrack)
            self._player_track = val
            track="track:"+self.playerTrack+". "
            print(track)
            try :
                if arduino_connected :
                    arduino.write(track.encode())
                    time.sleep(self.delay)
            except :
                logging.error("Error sending Track")

    @property
    def playerDuration(self):
        return self._player_duration

    @playerDuration.setter
    def playerDuration(self, val) :
        if not self._player_duration == val:
            logging.debug("Duration :%s", self.playerDuration)
            self._player_duration = val
            duration="duration:"+self.playerDuration
            print(duration)
            try :
                if arduino_connected :
                    arduino.write(duration.encode())
            except :
                logging.error("Error sending Duration")

    

    def run(self) :
        trial_error = 0
        trial_success = 0
        delay = 0.5
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
                        player["params"]={
                            "playerid":player_id,
                            "properties":["title","artist","albumartist","genre","year","album","track","duration"]
                        }
                        result = Extract(requests.post(host, headers=header, json=player).json())['result']['item']
                        self.playerTrack = str(result['track'])
                        self.playerTitle = result['title']

                        # self.playerType = Extract(result)['type']
                        # self.playerLabel = result['label']
                        
                        # self.playerArtist = result['artist'][0]
                        # self.playerAlbumArtist = result['albumartist'][0]
                        # self.playerGenre = result['genre'][0]
                        # self.playerYear = str(result['year'])
                        # self.playerAlbum = result['album']
                        
                        # self.playerDuration = str(result['duration'])
                        
                                                
                        time.sleep(delay)
                    except :
                        logging.error("error gathering player information")
                except :
                    trial_error += 1
                    trial_success = 0
                    if trial_error >= 5 :
                        break
                    logging.debug("no active player")
                
