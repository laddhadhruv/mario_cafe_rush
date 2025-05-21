from core.support import set_cutscene
from core.item import Item
from core.action import Action

class Keys(Item):
    def __init__(self):
        Item.__init__(self, "keys")    # do basic initialization for every item
        
        # build list of actions
        self.add_action(UnlockDoor)
    
    def get_description(self):
        return "keys"

# define actions for this item

class UnlockDoor(Action):
    def __init__(self):
        Action.__init__(self, "unlock_door")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Unlock Door"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"
    
    # only works in basement. add cutscene
    def do_action(self,game,room,request):
        if room.get_id() == 'basement':
            if room.treasure_locked:
                if room.lock_rusty:
                    set_cutscene("You try to turn the key but the lock appears to be rusted in place.")
                else:
                    set_cutscene("You turn the key and the lock turns with a grating sound.")
                    room.treasure_locked = False
            else:
                set_cutscene("The door is already unlocked.")
        else:
            set_cutscene("There are no locked doors here.")
        return 