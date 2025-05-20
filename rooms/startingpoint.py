from core.basehandler import BaseHandler
from core.room import Room
from core.action import Action

class StartingPoint(Room):
    
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        
        # build list of actions
        self.add_action(In)
    
    # return description of room.
    def get_description(self):
        return '''
        Today you are the barista, cook and baker on duty. Orders are piling up - can you survive the breakfast rush?
        '''
    # return image of room
    def get_image(self):
        return 'outside_cafe.png'
         
# define actions for this room

class In(Action):
    def __init__(self):
        Action.__init__(self, "In")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Get started"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'frontofhouse'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"