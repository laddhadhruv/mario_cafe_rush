from core.basehandler import BaseHandler
from core.room import Room
from items.keys import Keys
from core.action import Action

class Closet(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        
        # add inventory items
        self.add_item(Keys())
        
        # build list of actions
        self.add_action(Exit)
        self.add_action(ChooseShirt)
    
    # return description of room.
    def get_description(self):
        return "You are standing in a narrow closet.  There is not much room in here."
    
    # return image of room
    def get_image(self):
        return 'closet.jpg'


class ClosetHandler(BaseHandler):
    
    # return class to use to create a new instance of this room
    def get_room_class(self):
        return Closet

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

class ChooseShirt(Action):
    def __init__(self):
        Action.__init__(self, "ChooseShirt")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Choose Shirt"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'shirtchoice'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"

