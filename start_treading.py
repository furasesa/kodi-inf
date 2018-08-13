from threading_test import Host,Kodi
import time

h = Host("localhost:8080")
c = Kodi(args="JSONRPC.Ping",kwargs={"params":"testing"})

c.start()
time.sleep(1)
h.start()