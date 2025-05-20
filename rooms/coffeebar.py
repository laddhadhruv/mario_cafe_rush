from core.basehandler import BaseHandler
from core.room import Room
from items.keys import Keys
from core.action import Action

class CoffeeBar(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        
        # add inventory items
        self.add_item(Keys())
        
        # build list of actions
        self.add_action(ToFrontOfHouse)
        self.add_action(ToBakery)
        self.add_action(ToKitchen)
        # self.add_action(ChooseShirt)
    
    # return description of room.
    def get_description(self):
        return "You are at the coffee bar. Here you can prepare the drink orders."
    
    # return image of room
    def get_image(self):
        return 'coffee_bar.png'

class ClosetHandler(BaseHandler):
    
    # return class to use to create a new instance of this room
    def get_room_class(self):
        return CoffeeBar

# define actions for this room

# class ChooseShirt(Action):
#     def __init__(self):
#         Action.__init__(self, "ChooseShirt")    # do basic initialization for every action
    
#     # return description of action (used in label on webpage)
#     def get_description(self):
#         return "Choose Shirt"
    
#     # return id of room to enter when action is complete
#     def get_destination(self):
#         return 'shirtchoice'
    
#     # return http method to use when user clicks on this action
#     # use "get" if just moving to another room.  if changing something
#     # like the state of an inventory item or room then use "post"
#     def get_method(self):
#         return "get"

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
