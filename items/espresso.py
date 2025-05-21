from core.support import set_cutscene, get_game
from core.item import Item
from core.action import Action

class Espresso(Item):
    def __init__(self):
        super().__init__("espresso") # Initial ID
        self.base_id = "espresso"
        self.coffee_type_state = "espresso" # americano, cortado, cappuccino, latte
        self.has_sugar = False
        # self.has_milk = False # Redundant if using coffee_type_state for latte

        # build list of actions
        self.add_action(MakeLatte)
        self.add_action(MakeAmericano)
        self.add_action(MakeCortado)
        self.add_action(MakeCappuccino)
        self.add_action(AddSugarToEspresso) # New action for sugar
    
    def get_id(self):
        # ID should reflect the current state of the coffee
        current_id = self.coffee_type_state
        # If it's a derived drink (not base espresso), ensure it has "_drink" suffix for orders
        if self.coffee_type_state != "espresso" and not current_id.endswith("_drink"):
            current_id += "_drink"
        # If it's base espresso and has sugar, reflect that in ID for potential specific orders
        if self.coffee_type_state == "espresso" and self.has_sugar:
            # This makes the ID "espresso_with_sugar" which is unlikely to be directly ordered.
            # Orders will likely be for "espresso", and sugar is an optional add-on not changing the base item for order matching.
            # For simplicity with current order matching, let's not change ID for sugar on base espresso.
            # The description will still show "espresso with sugar".
            # If an order was specifically "espresso with sugar", we'd need OrderableCoffee(coffee_type="espresso_with_sugar")
            return self.base_id # Returns "espresso"
        return current_id

    def get_description(self):
        desc = self.coffee_type_state
        if self.coffee_type_state == "espresso" and self.has_sugar:
            desc += " with sugar"
        elif self.coffee_type_state != "espresso": # For derived drinks, don't add "with sugar" to desc for simplicity
            pass # Description is just the coffee type like "latte", "americano"
        return desc

# define actions for this item

class MakeLatte(Action):
    def __init__(self):
        Action.__init__(self, "make_latte") 
    
    def get_description(self):
        return "Make Latte"
    
    def get_method(self):
        return "post"
    
    def is_enabled(self):
        # Can only make latte from base espresso, prevent changing from another type
        return self.item.coffee_type_state == "espresso" and get_game().get_current_room().id == "coffeebar"
    
    def do_action(self,game,room,request):
        self.item.coffee_type_state = "latte" # This will become "latte_drink" via get_id()
        set_cutscene("You make a latte.")

class MakeAmericano(Action):
    def __init__(self):
        Action.__init__(self, "make_americano")
    
    def get_description(self):
        return "Make Americano"
    
    def get_method(self):
        return "post"
    
    def is_enabled(self):
        return self.item.coffee_type_state == "espresso" and get_game().get_current_room().id == "coffeebar"
    
    def do_action(self,game,room,request):
        self.item.coffee_type_state = "americano" # Becomes "americano_drink"
        set_cutscene("You make an americano.")

class MakeCortado(Action):
    def __init__(self):
        Action.__init__(self, "make_cortado")
    
    def get_description(self):
        return "Make Cortado"
    
    def get_method(self):
        return "post"
    
    def is_enabled(self):
        return self.item.coffee_type_state == "espresso" and get_game().get_current_room().id == "coffeebar"
    
    def do_action(self,game,room,request):
        self.item.coffee_type_state = "cortado" # Becomes "cortado_drink"
        set_cutscene("You make a cortado.")

class MakeCappuccino(Action):
    def __init__(self):
        Action.__init__(self, "make_cappuccino")
    
    def get_description(self):
        return "Make Cappuccino"
    
    def get_method(self):
        return "post"
    
    def is_enabled(self):
        return self.item.coffee_type_state == "espresso" and get_game().get_current_room().id == "coffeebar"
    
    def do_action(self,game,room,request):
        self.item.coffee_type_state = "cappuccino" # Becomes "cappuccino_drink"
        set_cutscene("You make a cappuccino.")

class AddSugarToEspresso(Action): # Renamed for clarity
    def __init__(self):
        Action.__init__(self, "add_sugar_to_espresso")
    
    def get_description(self):
        return "Add Sugar to Espresso"
    
    def get_method(self):
        return "post"

    def is_enabled(self):
        # Only allow adding sugar to a base espresso that doesn't already have sugar
        return self.item.coffee_type_state == "espresso" and not self.item.has_sugar and get_game().get_current_room().id == "coffeebar"

    def do_action(self,game,room,request):
        self.item.has_sugar = True
        set_cutscene("You add sugar to the espresso.")