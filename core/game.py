from core.player import Player
import core.support 

# the Game class stores the state of the game, which includes
# the current state of all rooms as well as the state of the player
class Game:
    def __init__(self):
        self.rooms = {}
        self.player = Player()
        self.history = []
        
    def get_player(self):
        return self.player
    
    def get_current_room(self):
        return self.history[-1] 
    
    def get_room(self,room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        return None
    
    # look for individual room object
    # if not found, then initialize room and store it
    def get_or_create_room(self,room_id,room_class):
        this_room = self.rooms.get(room_id)
        if not this_room:
            this_room = room_class(room_id)            
            self.rooms[room_id] = this_room
            self.update()        
        return this_room
    
    # save game state back into session
    def update(self):
        session = core.support.get_session()
        session['game'] = self
    
    # update history.  add room to end of list if it is not already there
    def update_history(self,room):
        if len(self.history) > 0:
            if self.history[-1].get_id() == room.get_id():
                return  # nothing to add
        
        # if we get here then the list is either empty or ends with a different room
        self.history.append(room)
