from core.item import Item
from core.action import Action

class Treasure(Item):
    def __init__(self):
        Item.__init__(self, "treasure")    # do basic initialization for every item
        
        # build list of actions
        self.add_action(EmergeVictorious)
    
    def get_description(self):
            return "a fabulous treasure"

# define actions for this item

class EmergeVictorious(Action):
    def __init__(self):
        Action.__init__(self, "emerge_victorious")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Emerge Victorious"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'victory_room'