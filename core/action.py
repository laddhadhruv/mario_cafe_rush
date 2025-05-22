# base class inherited by all actions
class Action:
    
    def __init__(self, action_id):
        self.id = action_id
    
    def get_id(self):
        return self.id
    
    # this method gets called when action executed.  can be overridden in subclass
    def do_action(self,game,room,request):
        return
    
    # should this action be available to player?
    # default is yes, but can be overridden.
    def is_enabled(self):
        return True
    
    # is this a navigation action?
    # we decide this based on whether the action has defined
    # a get_destination method
    def is_nav_action(self):
        return hasattr(self,'get_destination')
    
    # return description of action (used in label on webpage)
    # should be overridden in subclass with specific description
    def get_description(self):
        return "Action"
    
    # return http method to use when user clicks on an action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    #
    # if omitted in your action we return "post"
    def get_method(self):
        if self.is_nav_action():
            return "get"
        else:
            return "post"
        

# core/action.py
from core.support import set_cutscene


class DropItem(Action):
    def __init__(self):
        super().__init__("DropItem")

    def get_description(self):
        return "Drop Item"

    def get_method(self):
        return "post"

    def is_nav_action(self):
        # hide from the nav list — it’s triggered only via the inventory form
        return False

    def do_action(self, game, room, request):
        raw = request.form.get("drop_id")
        # convert to int if your keys are ints; otherwise leave as string
        try:
            drop_key = int(raw)
        except (TypeError, ValueError):
            drop_key = raw

        player = game.get_player()

        # 1) Does the player actually have this key?
        if drop_key not in player.inventory:
            set_cutscene("You don’t have that item.")
            return game, room.id

        item = player.inventory[drop_key]

        # 2) Enforce room‐specific drop
        section = getattr(item, "section", None)
        if section is None:
            set_cutscene("This item cannot be dropped.")
            return game, room.id

        if section != room.id:
            set_cutscene(f"You can only drop {item.get_description()} in the {section}.")
            return game, room.id

        # 3) All good — drop it
        player.inventory.pop(drop_key)
        set_cutscene(f"Dropped {item.get_description()}.")
        game.update()
        return game, room.id
