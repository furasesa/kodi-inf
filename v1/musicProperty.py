_track = None
_tittle = None
_artist = None
_album = None
_genre = None
_year = None
_duration = None

@property
def track ():
    return _track
@track.setter
def track (val):
    _track = val

@property
def title ():
    return _tittle
@title.setter
def title (val):
    _tittle = val

@property
def artist ():
    return _artist
@artist.setter
def artist (val):
    _artist = val

@property
def album ():
    return _album
@album.setter
def album (val):
    _album = val

@property
def genre ():
    return _genre
@genre.setter
def genre (val):
    _genre = val

@property
def year ():
    return _year
@year.setter
def year (val):
    _year = val

@property
def duration ():
    return _duration
@duration.setter
def duration (val):
    _duration = val

# message = [track,title,artist,album,genre,year,duration]
