import threading
import logging
import requests
import json
import time
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )

condition = threading.Condition()
header = {
            'Content-Type': 'application/json',
            'User-Agent': 'python-kodi'
        }        

class Extract(dict):
    # usage
    # d=Extract(dict)
    # d['arg']['kwarg']
    class NADict(object):
        def __getitem__(self, k):
            return "N/A"
    NA = NADict()
    def __missing__(self, k):
        return self.NA



def producer(host,username,password):
    trial_success = 0
    trial_error = 0
    while True:
        with condition:
            # logging.debug("host %s, username %s, password %s",host,username,password)
            ping = {
                "jsonrpc":"2.0",
                "method":"JSONRPC.Ping",
                "id":"ping"
            }
            try:
                known_host = Extract(requests.post(host, json=ping, auth=(username,password)).json())['result']
                if known_host=='pong':
                    trial_success += 1
                    # logging.debug("connected to %s",host)
                    if trial_success >= 5:
                        time.sleep(5)
                        trial_success = 0
                        break
                    condition.notifyAll()
            except:
                trial_error += 1
                if trial_error >= 5 :
                    sys.exit(1)
                logging.debug("error connection to %s, triying (%s)",host,trial_error)
        time.sleep(1)


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

def getPlayerExtractormation ():
    trial_error = 0
    trial_success = 0
    while True :
        with condition :
            condition.wait()
            params = {}
            params["jsonrpc"]="2.0"
            params["id"] = "playerExtract"
            params["method"] = "Player.GetActivePlayers"
            logging.debug("sending : %s to %s", params, host)
            try :
                player_type = Extract(requests.post(host, headers=header, json=params).json())['result'][0]['type']
                player_id = Extract(requests.post(host, headers=header, json=params).json())['result'][0]['playerid']
                trial_success += 1
                if trial_success >= 5 :
                    break
                logging.debug("id :%s, player : %s",player_id,player_type)
                if player_type == 'audio' :
                    params["method"]="Player.GetItem"
                    params["params"]={"playerid":player_id}
                    logging.debug("audio_Extract : %s",params)
                    audio_Extract = Extract(requests.post(host, headers=header, json=params).json())['result']['item']
                    logging.debug("audio_Extract : %s",audio_Extract)
            except :
                trial_error += 1
                if trial_error >= 5 :
                    break
                logging.debug("no active player")





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
    def run(self) :
        getPlayerExtractormation()


# def producer (cond,host):
#         logging.debug('producer : host %s',host)

# class Kodi (threading.Thread):
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
#         threading.Thread.__init__(self, group=group, target=target, name=name)
#         self.args = args
#         self.kwargs = kwargs
#         return

    # def producer (self,cond,host):
    #     logging.debug('producer')



    # def setHost(self,url,username="kodi",password="kodi"):
    #     self.host = "http://"+url+"/jsonrpc"
    #     self.username = username
    #     self.password = password
    #     global condition
    #     ping = {
    #         "jsonrpc":"2.0",
    #         "method":"JSONRPC.Ping",
    #         "id":"ping"
    #     }
    #     try:
    #         res = Extract(requests.post(self.host, json=ping, auth=(self.username,self.password)).json())['result']
    #         if res == "pong":
    #             with condition :
    #                 condition.notify_all()
    #                 logging.debug('conencted')
    #     except :
    #         logging.debug('failed connection to %s',self.host)
    #         sys.exit(1)
        

    # def run(self):
        # logging.debug("running thread")
        # header = {
        #     'Content-Type': 'application/json',
        #     'User-Agent': 'python-kodi'
        # }
        # params = {}
        # params['jsonrpc'] = '2.0'
        # params['id'] = self.id
        # params['method'] = self.args
        # if self.kwargs :
        #     params['params'] = self.kwargs

        # t = threading.currentThread()
        # with condition:
        #     logging.debug("waiting....")
        #     condition.wait()
        #     res = Extract(requests.post(self.host, headers=header, json=params, auth=(self.username,self.password)).json())['result']
        #     logging.debug('result : %s',res)

        # logging.debug('run args : %s, kwargs : %s',self.args,self.kwargs)
        # return



    
        
# def producer(cond,url,username='kodi',password='kodi'):
#     host = "http://"+url+"/jsonrpc"
#     header = {
#         'Content-Type': 'application/json',
#         'User-Agent': 'python-kodi'
#     }
#     ping = {
#         "jsonrpc":"2.0",
#         "method":"JSONRPC.Ping",
#         "id":"con"
#     }
#     logging.debug('starting coonection')
#     connnection = Extract(requests.post(host, headers=header, json=ping, auth=(username,password)).json())['result']
#     try:
#         if(connnection == 'pong'):
#             logging.debug("connection is available")
#             with cond:
#                 cond.notifyAll()
#                 logging.debug('Making resource available')
#     except:
#         loggin.debug("Please check your connection")
#         sys.exit(1)

# def consumer(cond):
#     """wait for the condition and use the resource"""
    
#     logging.debug('Starting consumer thread')
#     t = threading.currentThread()
#     with cond:
#         cond.wait()
#         logging.debug('Resource is available to consumer')



# condition = threading.Condition()
# host = "localhost:8080"
# c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
# c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
# p = threading.Thread(name='p', target=producer, args=(condition,"localhost:8080"))

# c1.start()
# time.sleep(1)
# c2.start()
# time.sleep(1)
# p.start()

# kodi = Kodi(args="JSONRPC.Ping",id="tc")
# condition = threading.Condition()
# host = "localhost:8080"
# ping = Kodi(name="ping", target=producer, args=(condition,host),kwargs={"JSONRPC.Ping"})
# ping.start()
# kodi = Kodi(args="Application.GetProperties", kwargs={"properties":["volume"]})
# kodi.setHost("localhost:8080")
# kodi.start()