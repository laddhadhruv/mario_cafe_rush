
# stores player info, especially inventory
class Player:
    def __init__(self):
        self.inventory = {}
    
    # adds item to the inventory for this player
    def add_item(self,item):
        
        self.inventory[item.get_id()] = item
        return
    
    # remove and return item from inventory (if it is there)
    # otherwise return empty string
    def pop_item(self,item_id):
        
        return self.inventory.pop(item_id,'')