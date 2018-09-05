import requests

class Extract(dict):
    class NADict(object):
        def __getitem__(self, k):
            return "N/A"
    NA = NADict()
    def __missing__(self, k):
        return self.NA

ping = {
        "jsonrpc" : "2.0",
        "method" : "JSONRPC.Ping",
        "id" : "ping"
    }
host = "http://192.168.43.165:8080/jsonrpc"
known_host = Extract(requests.post(host, json=ping).json())['result']
print(known_host)

t1 = {
    "jsonrpc" : "2.0",
    "method" : "Player.GetProperties",
    "id" : "gp",
    "params":{
        "playerid":0,
        "properties":["percentage"]
        }
    }
r1 = Extract(requests.post(host, json=t1).json())['result']['percentage']
print (r1)


playeritem={
    "jsonrpc" : "2.0",
    "method" : "Player.GetItem",
    "id" : "gp",
    "params":{
        "playerid":0,
        "properties":["title","artist","albumartist","genre","year","album","track","duration"]
        }
}
result = Extract(requests.post(host, json=playeritem).json())['result']['item']
ptype = result['type']
title = result['title']
artist = result['artist'][0]
albumartist = result['albumartist'][0]
genre = result['genre'][0]
year = result['year']
album = result['album']
track = result['track']
duration = result['duration']
print ("type:",ptype,"title:",title," artist:",artist,"albumartist:",albumartist,"genre:",genre,"year:",year,
"album:",album,"track:",track,"duration:",duration)

