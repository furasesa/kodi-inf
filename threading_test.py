import threading
import logging
import requests
import json
import time
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )
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

condition = threading.Condition()

def producer(host,username,password):
    with condition:
        # logging.debug("host %s, username %s, password %s",host,username,password)
        ping = {
            "jsonrpc":"2.0",
            "method":"JSONRPC.Ping",
            "id":"ping"
        }
        try:
            known_host = Inf(requests.post(host, json=ping, auth=(username,password)).json())['result']
            if known_host=='pong':
                logging.debug("connected to %s",host)
                condition.notifyAll()
        except:
            logging.debug("error connection to %s",host)
            sys.exit(1)


def consumer(args,kwarg):
    with condition :
        logging.debug("waiting host")
        condition.wait()
        logging.debug("args %s, kwargs %s",args,kwarg)

class Host(threading.Thread):
    def __init__(self, url, username="kodi", password="kodi"):
        threading.Thread.__init__(self)
        self.host = "http://"+url+"/jsonrpc"
        self.username = username
        self.password = password

    def run (self):
        logging.debug("running host")
        producer(self.host,self.username,self.password)

class Kodi(threading.Thread):
    def __init__(self, args=(), kwargs=None, target=None, name=None):
        threading.Thread.__init__(self, args=(), kwargs=None, target=None, name=None)
        self._args = args
        self._kwargs = kwargs
    def run(self):
        logging.debug("running Kodi")
        consumer(self._args,self._kwargs)





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
    #         res = Inf(requests.post(self.host, json=ping, auth=(self.username,self.password)).json())['result']
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
        #     res = Inf(requests.post(self.host, headers=header, json=params, auth=(self.username,self.password)).json())['result']
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
#     connnection = Inf(requests.post(host, headers=header, json=ping, auth=(username,password)).json())['result']
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