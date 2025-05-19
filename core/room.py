# base class inherited by all rooms
class Room:
    
    def __init__(self, room_id):
        self.id = room_id
        self.inventory = {}
        self.actions = {}
    
    # adds item to the inventory for this room
    def add_item(self,item):
        
        self.inventory[item.get_id()] = item
        return
    
    # remove and return item from inventory (if it is there)
    # otherwise return empty string
    def pop_item(self,item_id):
        
        return self.inventory.pop(item_id,'')
    
    # adds action to the actions list for this room
    def add_action(self,action_class):
        
        new_action = action_class()
        new_action.room = self
        self.actions[new_action.get_id()] = new_action
        return
    
    # return id of room.
    def get_id(self):
        return self.id
    
    # return description of room.  this should be overridden in subclasses
    def get_description(self):
        return "You are standing in a room."
    
    # get image of room.  by default no image is returned.
    # override in subclass to return an image 
    def get_image(self):
        return None