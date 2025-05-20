from core.basehandler import BaseHandler
from core.room import Room
from items.oilcan import OilCan
from items.lamp import Lamp
from core.action import Action

class FrontOfHouse(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        
        # add inventory items
        self.add_item(Lamp())
        self.add_item(OilCan())
        
        # build list of actions
        self.add_action(Out)
        self.add_action(ToBakery)
        self.add_action(ToCoffeeBar)
        self.add_action(ToKitchen)
    
    # return description of room.
    def get_description(self):
        return "Welcome to Café Byte. Let's start working on the open orders."
    
    # return image of room
    def get_image(self):
        return 'entrance_cafe.png'

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

class ToBakery(Action):
    def __init__(self):
        Action.__init__(self, "ToBakery")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter the bakery"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'bakery'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
class ToKitchen(Action):
    def __init__(self):
        Action.__init__(self, "ToKitchen")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter the kitchen"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'kitchen'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
class ToCoffeeBar(Action):
    def __init__(self):
        Action.__init__(self, "ToCoffeeBar")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter the coffee bar"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'coffeebar'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"