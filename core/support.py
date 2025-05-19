from flask import Flask, session
import urllib.parse
from core.game import Game
from core.basehandler import BaseHandler

# Register Handlers at the top level:
_handlers = dict()
def registerHandler(app:Flask, room_class:type, room_id:str, template:str="room.html", handler_class:type=BaseHandler):
    global _handlers # access module's _handlers variable
    if room_id not in _handlers:
        handler = handler_class(app, room_class, room_id, template)
        _handlers[room_id] = handler
    else:
        handler = _handlers[room_id]
    return handler

def registerForm(app:Flask, form_id:str, template:str, handler_class:type):
    global _handlers # access module's _handlers variable
    if form_id not in _handlers:
        handler = handler_class(app, form_id, template)
        _handlers[form_id] = handler
    else:
        handler = _handlers[form_id]
    return handler

def get_session():
    return session

# store text as cutscene to be used in next room display
def set_cutscene(content):
    session = get_session()    # find or create the session
    session['cutscene'] = content

# called when cutscene is going to be displayed
# if there is a cutscene return that and clear cutscene
# otherwise just return empty string
def play_cutscene():
    session = get_session()    # find or create the session
    cutscene = session.get('cutscene','')
    if cutscene != '':
        session['cutscene'] = ''
    return cutscene

# get_game() returns game object
#
# we use the variable cur_game which is defined in 
# the namespace of this module (support.py) to store
# the game object.  this allows us to ensure that there is
# always at most one game object in play.  otherwise if
# multiple get_game() requests are made when processing a single
# request, changes made to one game object can overwrite
# those made in another.
#
# get_game first checks to see if there is already a game object
# stored in cur_game, in which case it returns that.  otherwise,
# retrieve game object from session.  if there is no game object
# stored yet, create one.  store game object in cur_game

_cur_game = None     # note that this variable must be defined oustide get_game so it is in the module namespace
def get_game():
    global _cur_game     # access module's cur_game variable
    # get game object if we don't have it
    if not _cur_game:
        session = get_session()    # find or create the session
        _cur_game = session.get('game','')
        if not _cur_game:
            _cur_game = Game()
            session['game'] = _cur_game
    return _cur_game

# reset game by clearing session and also clearing cur_game variable
def reset_game():
    global _cur_game
    _cur_game = None
    
    session = get_session()    # find or create the session

    # delete all keys from session
    session.clear()
    # For original session implementation:
    #cur_keys = session.session.keys()
    #for key in cur_keys:
    #    session.delete_item(key)

# turn a string into a path by prefixing a "/" and escaping any special characters
def get_path(path_text):
    return "/" + urllib.parse.quote(path_text)

