import uuid # Import the uuid module
from flask import current_app
# stores player info, especially inventory
class Player:
    def __init__(self):
        self.inventory = {} # Will store {unique_uuid_key: item_object}
        self.name = current_app.config.get('player_name', 'Guest')

    def update_name(self):
        self.name = current_app.config.get('player_name', 'Guest')
    
    # adds item to the inventory for this player
    def add_item(self,item):
        unique_key = uuid.uuid4().hex # Generate a unique key for the inventory dictionary
        self.inventory[unique_key] = item
        return
    
    # remove and return item from inventory (if it is there)
    def pop_item(self,item_id_to_pop):
        key_to_remove = None
        item_to_return = None

        # Ensure item_id_to_pop is a string for comparison, though it should be.
        str_item_id_to_pop = str(item_id_to_pop)

        for key, item_obj in self.inventory.items():
            # Ensure the item's current ID is also treated as a string for comparison.
            current_item_id = str(item_obj.get_id())
            if current_item_id == str_item_id_to_pop:
                key_to_remove = key
                break
        
        if key_to_remove:
            item_to_return = self.inventory.pop(key_to_remove)
            return item_to_return
            
        return '' # Item not found by its current get_id()