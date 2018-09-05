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
host = "http://localhost:8080/jsonrpc"
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