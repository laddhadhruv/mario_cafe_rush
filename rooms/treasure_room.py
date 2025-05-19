from core.basehandler import BaseHandler
from core.room import Room
from core.action import Action
from items.treasure import Treasure

class TreasureRoom(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        
        # add inventory items
        self.add_item(Treasure())
        
        # build list of actions
        self.add_action(Exit)
    
    # return description of room.
    def get_description(self):
        return "You are standing in a treasure room overflowing with bars of gold, jewels, crowns, and scepters."
    
    # return image of room
    def get_image(self):
        return 'treasure_room.jpg'

# define actions for this room

class Exit(Action):
    def __init__(self):
        Action.__init__(self, "Exit")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Exit"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'basement'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"

