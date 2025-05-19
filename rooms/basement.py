from core.basehandler import BaseHandler
from core.room import Room
from core.support import set_cutscene, get_game
from core.action import Action

class Basement(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        self.treasure_locked = True
        self.lock_rusty = True
        
        # build list of actions
        self.add_action(Up)
        self.add_action(East)
        self.add_action(South)
    
    def get_description(self):
        if self.is_illuminated():
            desc = '''
            You are in a dank basement. The walls are concrete with remnants of what looks like wood paneling.  
            There is a large door on the south wall and a small door to the east.
            '''
        else:
            desc = "You are in what feels like a dank basement.  It is pitch dark."
        return desc
    
    def get_image(self):
        if self.is_illuminated():
            return 'basement-lit.jpg'
        else:
            return 'basement.jpg'
    
    # report whether this room is illuminated
    # which can happen if the room or player has a lit lamp
    def is_illuminated(self):
        
        game = get_game()
        
        # is there a lit lamp in the room itself?
        if 'lamp' in self.inventory:
            if self.inventory['lamp'].is_lit:
                return True
        
        # does the player have a lit lamp?
        player = game.get_player()
        if 'lamp' in player.inventory:
            if player.inventory['lamp'].is_lit:
                return True
                
        # if we get here, the lamp is not lit
        return False

# define actions for this room

class Up(Action):
    def __init__(self):
        Action.__init__(self, "Up")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Go Upstairs"
    
    # set cutscene for when arrive in entrance_hall
    def do_action(self,game,room,request):
        set_cutscene("You hear a clanging sound from behind you as you climb the stairs.")
        return
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'entrancehall'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"

class East(Action):
    def __init__(self):
        Action.__init__(self, "East")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Go East"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'closet'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
    # enabled only if room is lit.
    def is_enabled(self):
        if self.room.is_illuminated():
            return True
        else:
            return False

class South(Action):
    def __init__(self):
        Action.__init__(self, "South")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Go South"
    
    # if treasure is unlocked we go into that room
    # otherwise stay in the basement
    def get_destination(self):
        if self.room.treasure_locked:
            return 'basement'
        else:
            return 'treasure_room'
    
    # set cutscene for when arrive in entrance_hall
    def do_action(self,game,room,request):
        if self.room.treasure_locked:
            set_cutscene("You can't enter that room because the door is locked.")
        return
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
    # enabled only if room is lit.
    def is_enabled(self):
        if self.room.is_illuminated():
            return True
        else:
            return False