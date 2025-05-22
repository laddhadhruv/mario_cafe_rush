from core.basehandler import BaseHandler
from core.room import Room
from core.action import Action
# from items.treasure import Treasure # No longer used
from items.orderable_items import Egg, Bacon # Import new items
from core.action import DropItem

# inside Kitchen.__init__:
   


class Kitchen(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        self.add_action(DropItem)
        # Add items available in the kitchen
        self.add_item(Egg(style="scrambled")) # scrambled_egg
        self.add_item(Egg(style="boiled"))    # boiled_egg
        self.add_item(Egg(style="omelette"))  # omelette_egg
        self.add_item(Bacon(cooking_style="soft"))    # soft_bacon
        self.add_item(Bacon(cooking_style="crispy"))  # crispy_bacon
        
        # build list of actions
        # self.add_action(Exit)
        self.add_action(ToFrontOfHouse)
        self.add_action(ToCoffeeBar)
        self.add_action(ToBakery)
    
    # return description of room.
    def get_description(self):
        return "You are in the kitchen now. Here you can prepare sandwiches by preparing and adding ingredients."
    
    # return image of room
    def get_image(self):
        return 'kitchen.png'

# define actions for this room

class ToFrontOfHouse(Action):
    def __init__(self):
        Action.__init__(self, "Enter Front-of-House")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter Front-of-House"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'frontofhouse'
    
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




# class Exit(Action):
#     def __init__(self):
#         Action.__init__(self, "Exit")    # do basic initialization for every action
    
#     # return description of action (used in label on webpage)
#     def get_description(self):
#         return "Exit"
    
#     # return id of room to enter when action is complete
#     def get_destination(self):
#         return 'basement'
    
#     # return http method to use when user clicks on this action
#     # use "get" if just moving to another room.  if changing something
#     # like the state of an inventory item or room then use "post"
#     def get_method(self):
#         return "get"

