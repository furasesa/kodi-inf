from kodiinf import Kodi, Inf
import threading
import queue
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


# delay = 100
# exitFlag = 0
# class KodiService(threading.Thread):
#     def __init__ (self, kodi,threadId, name, queue):
#         threading.Thread.__init__(self)
#         self.threadId = threadId
#         self.name = name
#         self.kodi = kodi
#         self.queue = queue

#     def run (self):
#         # logging.debug("starting")
#         proccess_data(self.name, self.queue)

# def proccess_data (threadName,queue):
#     while not exitFlag:
#       queueLock.acquire()
#       if not workQueue.empty():
#          data = queue.get()
#          queueLock.release()
#          logging.debug ("%s processing %s" % (threadName, data))
#       else:
#          queueLock.release()
#          time.sleep(1)


# def get_music_player_info (self):
#     try :
#         getActivePlayers = kodi.setData("Player.GetActivePlayers")
#         playerid = kodi.getResult(getActivePlayers)[0]['playerid']
#     except :
#         pass


# threadList = ["get_player_info","time_info"]
# queueLock = threading.Lock()
# workQueue = queue.Queue(10)
# threads = []
# threadID = 1

# kodi = Kodi("localhost:8080")
# # playerService = KodiService(kodi, 1 ,"music-info")
# # playerService.start()

# # Create new threads
# for tName in threadList:
#    thread = KodiService(kodi,threadID,tName,workQueue)
#    thread.start()
#    threads.append(thread)
#    threadID += 1

# # Fill the queue
# queueLock.acquire()
# for word in threadList:
#    workQueue.put(word)
# queueLock.release()

# # Wait for queue to empty
# while not workQueue.empty():
#    pass

# # Notify threads it's time to exit
# exitFlag = 1

# # Wait for all threads to complete
# for t in threads:
#    t.join()
# print ("Exiting Main Thread")

def consumer(cond):
    """wait for the condition and use the resource"""
    logging.debug('Starting consumer thread')
    t = threading.currentThread()
    with cond:
        cond.wait()
        logging.debug('Resource is available to consumer')


def connection(cond):
    """set up the resource to be used by the consumer"""
    # logging.debug('Starting producer thread')
    successfull_tries = 0
    with cond:
        logging.debug('Making resource available')
        cond.notify()
        # cond.notifyAll()


condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
# c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
con = threading.Thread(name='con', target=connection, args=(condition,))

c1.start()
# time.sleep(2)
# c2.start()
# time.sleep(2)
con.start()
