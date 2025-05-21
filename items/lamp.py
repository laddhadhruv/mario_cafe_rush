from core.support import set_cutscene
from core.item import Item
from core.action import Action

class Lamp(Item):
    def __init__(self):
        Item.__init__(self, "lamp")    # do basic initialization for every item
        self.is_lit = False
        
        # build list of actions
        self.add_action(TurnOn)
        self.add_action(TurnOff)
    
    def get_description(self):
        if self.is_lit:
            return "lamp (shining brightly)"
        else:
            return "lamp (off)"


# define actions for this item

class TurnOn(Action):
    def __init__(self):
        Action.__init__(self, "turn_on")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Turn Lamp On"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"
    
    # enabled only if lamp is off.
    def is_enabled(self):
        return not self.item.is_lit
    
    # turn lamp on and add cutscene
    def do_action(self,game,room,request):
        self.item.is_lit = True
        set_cutscene("You press the switch on the lamp and it begins to glow brightly.")

class TurnOff(Action):
    def __init__(self):
        Action.__init__(self, "turn_off")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Turn Lamp Off"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"
    
    # enabled only if lamp is on.
    def is_enabled(self):
        return self.item.is_lit
    
    # turn lamp on and add cutscene
    def do_action(self,game,room,request):
        self.item.is_lit = False
        set_cutscene("You press the switch on the lamp and it goes dark.") 