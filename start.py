from kodiinf import Kodi

kodi = Kodi("localhost:8080")

def Player():
    getActivePlayers = kodi.setData("Player.GetActivePlayers")
    playerid = kodi.getResult(getActivePlayers)[0]['playerid']
    # print(kodi.getResult(getActivePlayers)[0]['playerid'])
    # if (type(kodi.getResult(getActivePlayers) is list)):
    #     print("is a list")
    # getItems = kodi.setData("Player.GetItem",{"playerid":playerid})
    # print(getItems)
    # getLabel = kodi.getResult(getItems)['item']['label']
    # print(getLabel)

    getProps = kodi.setData("Player.GetItem",{ "properties": ["title", "album", "artist", "duration", "thumbnail", "file", "fanart", "streamdetails"],"playerid":playerid})
    getTitle = kodi.getResult(getProps)['item']['title']
    print(getTitle)
    getAlbum = kodi.getResult(getProps)['item']['album']
    print(getAlbum)
    getArtist = kodi.getResult(getProps)['item']['artist']
    print(getArtist)
    getDuration = kodi.getResult(getProps)['item']['duration']
    print(getDuration)
    
    

if __name__ == "__main__":
    
    # isMute = kodi.setData("Application.SetMute",{"mute":False})
    # print(kodi.getResult(isMute))
    # if(isMute):
    #     print("Kodi is Mute")
    # ping = kodi.setData("JSONRPC.Ping")
    # print(kodi.getResult(ping))

    # getSong = kodi.setData("AudioLibrary.GetSongs")
    # print(kodi.getResult(getSong))

    # vol = kodi.setData("Application.GetProperties",{"properties":["volume"]})
    # print(kodi.getResult(vol)['volume'])

    Player()