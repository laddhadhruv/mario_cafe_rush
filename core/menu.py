import collections

# menu collects actions that should be displayed on current page
class Menu:
    def __init__(self):
        self.actions = {}
    
    # build menu of actions from a room and player object
    # the actions are stored in self.actions
    def build_menu(self,room,player):
        
        actions = {}
        
        # start by adding all enabled actions from room to the menu
        if hasattr(room,'actions'):
            room_actions = room.actions.values()
            for action in room_actions:
                if action.is_enabled():
                    actions[action.get_id()] = action
        
        # now add all actions from each object in player's inventory
        items = player.inventory.values()
        for item in items:
            if hasattr(item,'actions'):
                item_actions = item.actions.values()
                for action in item_actions:
                    if action.is_enabled():
                        actions[action.get_id()] = action
        
        #Sort the actions by id so they are consistent:
        actions = collections.OrderedDict(sorted(actions.items()))
        
        # save menu in actions attribute
        self.actions = actions
        