import requests
import json
import sys

# version 0.1

class Inf(dict):
    # usage
    # d=Inf(dict)
    # d['arg']['kwarg']
    class NADict(object):
        def __getitem__(self, k):
            return "N/A"
    NA = NADict()
    def __missing__(self, k):
        return self.NA

class Kodi (object):
    def __init__(self,url,username="Kodi",password="xbmc",debug=False):
        self.host = "http://"+url+"/jsonrpc"
        self.username = username
        self.password = password
        self.header = {
            'Content-Type': 'application/json',
            'User-Agent': 'python-kodi'
        }
        self.id = 0
        # self.response = {}

        ping = {
            "jsonrpc":"2.0",
            "method":"JSONRPC.Ping",
            "id":"con"
        }
        try :
            testconnection = Inf(requests.post(self.host, headers=self.header, json=ping, auth=(self.username,self.password)).json())['result']
            if debug :
                if (testconnection=='pong'):
                    print("connection OK")
                    # self.isConnected == True
        except:
            print("Please check your connection")
            sys.exit(1)

    # def checkConnection(self):
    #     if(self.isConnected):
    #         return True
    
    def setData (self,method,params=None):
        data = {
            "jsonrpc":"2.0"
        }
        data['method'] = method
        if(params):
            data['params'] = params
        self.id += 1
        data['id'] = self.id
        self.response = requests.post(self.host, headers=self.header, json=data,auth=(self.username,self.password)).json()
        # print(self.response)
        return self.response

    def getResult(self,sresponse):
        # usage :
        # if response 'result' : OK => kodi.getResult(sresponse)
        # {'id': 1, 'jsonrpc': '2.0', 'result': {'volume': 100}}  => kodi.getResult(sresponse)['volume']
        return Inf(sresponse)['result']

# if __name__ == "__main__":
    # test code
    # kodi = Kodi("localhost:8080") 
    # vol = kodi.setData("Application.GetProperties", {"properties":["volume"]})
    # kodiquit = kodi.setData("Application.Quit")
    # print (kodi.getResult(vol)['volume'])
    
    
    
