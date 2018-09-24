# import queue
# import threading

# def basic_worker(queue,kw):
#     while True:
#         item = queue.get()
#         # do_work(item)
#         print(item,kw)
#         queue.task_done()
# def basic():
#     # http://docs.python.org/library/queue.html
#     q = queue.Queue()
    
#     for i in range(3):
#          t = threading.Thread(target=basic_worker,args=(q,"{sdqw:ww}"))
#          t.daemon = True
#          t.start()
#     for item in range(4):
#         q.put(item)
#     q.join()       # block until all tasks are done
#     print('got here')

# basic()

a = list("asdqwf3")
print(a, len(a))
b = a[0:5]
str_b = ''.join(b)
print (str_b)
