from core.support import set_cutscene, get_game
from core.item import Item
from core.action import Action

class Espresso(Item):
    def __init__(self):
        super().__init__("espresso")        # Initial ID
        self.section            = "coffeebar"  # ← allow dropping only in the coffee bar
        self.base_id            = "espresso"
        self.coffee_type_state  = "espresso"   # americano, cortado, cappuccino, latte
        self.has_sugar          = False
        self.set_is_generator(True)          # This is an espresso MACHINE

        # build list of actions
        self.add_action(MakeLatte)
        self.add_action(MakeAmericano)
        self.add_action(MakeCortado)
        self.add_action(MakeCappuccino)
        self.add_action(AddSugarToEspresso)

    def reset_to_default_state(self):
        # Fresh espresso dispensed: reset to base state
        self.coffee_type_state = "espresso"
        self.has_sugar         = False
        self.set_is_generator(False)
        # Preserve the correct description
        self.description = self.get_description()

    def get_id(self):
        # ID reflects current drink type, ends with "_drink"
        current_id = self.coffee_type_state
        if not current_id.endswith("_drink"):
            current_id += "_drink"
        return current_id

    def get_description(self):
        desc = self.coffee_type_state
        if desc.endswith("_drink"):
            desc = desc[:-6]
        if self.coffee_type_state == "espresso" and self.has_sugar:
            desc += " with sugar"
        return desc

# ─── Actions for Espresso ─────────────────────────────────

class MakeLatte(Action):
    def __init__(self):
        super().__init__("make_latte")
    def get_description(self):
        return "Make Latte"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return (self.item.coffee_type_state == "espresso"
                and get_game().get_current_room().id == "coffeebar")
    def do_action(self, game, room, request):
        self.item.coffee_type_state = "latte"
        set_cutscene("You make a latte.")

class MakeAmericano(Action):
    def __init__(self):
        super().__init__("make_americano")
    def get_description(self):
        return "Make Americano"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return (self.item.coffee_type_state == "espresso"
                and get_game().get_current_room().id == "coffeebar")
    def do_action(self, game, room, request):
        self.item.coffee_type_state = "americano"
        set_cutscene("You make an americano.")

class MakeCortado(Action):
    def __init__(self):
        super().__init__("make_cortado")
    def get_description(self):
        return "Make Cortado"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return (self.item.coffee_type_state == "espresso"
                and get_game().get_current_room().id == "coffeebar")
    def do_action(self, game, room, request):
        self.item.coffee_type_state = "cortado"
        set_cutscene("You make a cortado.")

class MakeCappuccino(Action):
    def __init__(self):
        super().__init__("make_cappuccino")
    def get_description(self):
        return "Make Cappuccino"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return (self.item.coffee_type_state == "espresso"
                and get_game().get_current_room().id == "coffeebar")
    def do_action(self, game, room, request):
        self.item.coffee_type_state = "cappuccino"
        set_cutscene("You make a cappuccino.")

class AddSugarToEspresso(Action):
    def __init__(self):
        super().__init__("add_sugar_to_espresso")
    def get_description(self):
        return "Add Sugar to Espresso"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return (self.item.coffee_type_state == "espresso"
                and not self.item.has_sugar
                and get_game().get_current_room().id == "coffeebar")
    def do_action(self, game, room, request):
        self.item.has_sugar = True
        set_cutscene("You add sugar to the espresso.")
