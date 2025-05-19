from core.support import set_cutscene
from core.item import Item
from core.action import Action

class OilCan(Item):
    def __init__(self):
        Item.__init__(self, "oil can")    # do basic initialization for every item
        self.has_oil = True
                
        # build list of actions
        self.add_action(ApplyOil)
    
    def get_description(self):
            return "oil can"

# define actions for this item

class ApplyOil(Action):
    def __init__(self):
        Action.__init__(self, "apply_oil")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Apply Oil"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"
    
    # only works in basement. add cutscene
    def do_action(self,game,room,request):
        if self.item.has_oil:
            if room.get_id() == 'basement':
                if room.lock_rusty:
                    set_cutscene("You squirt some oil on the lock on the large door.")
                    self.item.has_oil = False
                    room.lock_rusty = False
            else:
                set_cutscene("You squeeze the oil can and a jet of oil streams on to the floor.  The oil can is now empty.  There is a small pool of oil on the floor.")
                self.item.has_oil = False
        else:
            set_cutscene("You squeeze the oil can, but it is empty.")
        return