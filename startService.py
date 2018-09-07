from kodiService import Host,Player,Kodi

host = Host("localhost:8080")
player = Player()
player.setName("player")
# k = Kodi(args="Player.id")

host.start()
player.start()
# k.start()



# from gatherInformation import MyKodi

# m = MyKodi()
# m.Host("localhost:8080")
# m.host = "localhost:8080"
# m.start()