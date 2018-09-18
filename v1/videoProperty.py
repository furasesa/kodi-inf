_videotype = None
_showtitle = None
_season = None
_episode = None
_title = None
_votes = None

@property
def videoType():
    return _videotype
@videoType.setter
def videoType(v):
    _videotype = v

@property
def showTitle():
    return _showtitle
@showTitle.setter
def showTitle(v):
    _showtitle = v

@property
def season():
    return _season
@season.setter
def season(v):
    _season = v

@property
def episode():
    return _episode
@episode.setter
def episode(v):
    _episode = v

@property
def title():
    return _title
@title.setter
def title(v):
    _title = v

@property
def votes():
    return _votes
@votes.setter
def votes(v):
    _votes = v