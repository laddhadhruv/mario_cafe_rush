# base class inherited by all items
class Item:
    
    def __init__(self, item_id):
        self.id = item_id
        self.actions = {}
        self.description = "A plain vanilla item"
        self.is_generator = False
    
    def get_id(self):
        return self.id
    
    # display description of item.
    # should be overridden in subclass.
    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description
    
    def set_is_generator(self, is_generator: bool):
        self.is_generator = is_generator
    
    # adds action to the actions list for this item
    def add_action(self,action_class):
        
        new_action = action_class()
        new_action.item = self
        self.actions[new_action.get_id()] = new_action
        return
    
    # action to take when item is added to player inventory
    # (no action by default; override in subclass as needed)
    def do_item_added(self,game,room,request):
        return
    
    # action to take when item is dropped from player inventory
    # (no action by default; override in subclass as needed)
    def do_item_dropped(self,game,room,request):
        return
