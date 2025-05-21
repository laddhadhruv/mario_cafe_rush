from core.support import set_cutscene, get_game
from core.item import Item
from core.action import Action

class Coffee(Item):
    def __init__(self):
        Item.__init__(self, "coffee")    # do basic initialization for every item
        
        self.has_sugar = False
        self.has_milk = False

        # build list of actions
        self.add_action(TakeCoffee)
        self.add_action(AddSugar)
        self.add_action(AddMilk)
    
    def get_description(self):
        if self.has_sugar and self.has_milk:
            return "coffee with milk and sugar"
        elif self.has_sugar:
            return "coffee with sugar"
        elif self.has_milk:
            return "coffee with milk"
        else:
            return "coffee"

# define actions for this item

class TakeCoffee(Action):
    def __init__(self):
        Action.__init__(self, "take_coffee")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Take Coffee"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"

class AddSugar(Action):
    def __init__(self):
        Action.__init__(self, "add_sugar")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Add Sugar"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"
    
    # enabled only if lamp is off.
    def is_enabled(self):
        return not self.item.has_sugar and get_game().get_current_room().id == "coffeebar"
    
    # turn lamp on and add cutscene
    def do_action(self,game,room,request):
        self.item.has_sugar = True
        set_cutscene("You add sugar to the coffee.")

class AddMilk(Action):
    def __init__(self):
        Action.__init__(self, "add_milk")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Add Milk"
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "post"
    
    # enabled only if lamp is off.
    def is_enabled(self):
        return not self.item.has_milk and get_game().get_current_room().id == "coffeebar"
    
    # turn lamp on and add cutscene
    def do_action(self,game,room,request):
        self.item.has_milk = True
        set_cutscene("You add milk to the coffee.")