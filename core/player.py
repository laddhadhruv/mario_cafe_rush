import uuid # Import the uuid module
from flask import current_app
import os 
import json

# Define CONFIG_PATH here or ensure it's accessible
# This is a bit of a hack, ideally config path comes from a central place
# For now, assuming it's consistent with main.py
CONFIG_PATH = '/tmp/config.json' 

# stores player info, especially inventory
class Player:
    def __init__(self):
        self.inventory = {} # Will store {unique_uuid_key: item_object}
        player_name_from_file = None
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, 'r') as f:
                    cfg_from_file = json.load(f)
                    player_name_from_file = cfg_from_file.get('player_name')
        except Exception: # Broad exception if file is malformed or other issues
            # If there's an issue reading the file (e.g., during a write, or malformed)
            # it's better to log this and fall back rather than crash.
            # For now, just pass and allow fallback.
            pass

        if player_name_from_file:
            self.name = player_name_from_file
        else:
            # Fallback to app.config, then to 'Guest'
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