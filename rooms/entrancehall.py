from core.basehandler import BaseHandler
from core.room import Room
from items.oilcan import OilCan
from items.lamp import Lamp
from core.action import Action

class EntranceHall(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        
        # add inventory items
        self.add_item(Lamp())
        self.add_item(OilCan())
        
        # build list of actions
        self.add_action(Out)
        self.add_action(Down)
    
    # return description of room.
    def get_description(self):
        return "You are standing in a gloomy entrance hall."
    
    # return image of room
    def get_image(self):
        return 'entrance_hall.jpg'

# define actions for this room

class Out(Action):
    def __init__(self):
        Action.__init__(self, "Out")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Go Outside"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'startingpoint'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"


class Down(Action):
    def __init__(self):
        Action.__init__(self, "Down")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Go Downstairs"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'basement'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"