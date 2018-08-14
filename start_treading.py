from threading_test import Host,Kodi, Extract, Player
import time

h = Host("localhost:8080")
c = Kodi(id="gvol", args="Application.GetProperties",kwargs={"properties":["volume"]}, getresult="volume")
c.setName("get_volume")
# s = Kodi(name="getPlayer", id="gPlayer", args="Player.GetActivePlayers")
mute = Kodi(id="setMute",args="Application.SetMute",kwargs={"mute":True})
mute.setName("mute")

player = Player()
player.setName("player")

h.start()
c.start()
time.sleep(1)
mute.start()
time.sleep(1)
player.start()
time.sleep(1)
