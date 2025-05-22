from core.basehandler import BaseHandler
from core.room import Room
# from items.coffee import Coffee # No longer used
from items.espresso import Espresso
from core.action import Action
from core.action import DropItem

# inside CoffeeBar.__init__:
    

class CoffeeBar(Room):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.add_action(DropItem)
        # add inventory items
        # self.add_item(Coffee()) # No longer used
        self.add_item(Espresso())    

        # build list of actions
        self.add_action(ToFrontOfHouse)
        self.add_action(ToBakery)
        self.add_action(ToKitchen)

        # control inline form visibility
        self.show_order_form = False

    def get_description(self):
        return "You are at the coffee bar. Here you can prepare the drink orders."

    def get_image(self):
        return 'coffee_bar.png'

class CoffeeBarHandler(BaseHandler):
    def get_room_class(self):
        return CoffeeBar

    # override GET to ensure your template is used
    def handle_get(self, game, room, request):
        # Reset form flag on a fresh GET
        room.show_order_form = False
        return self.render('coffeebar.html')

# ─── Navigation Actions ─────────────────────────────────

class ToFrontOfHouse(Action):
    def __init__(self):
        super().__init__("EnterFrontHouse")
    def get_description(self):
        return "Enter Front-of-House"
    def get_destination(self):
        return 'frontofhouse'
    def get_method(self):
        return "get"

class ToBakery(Action):
    def __init__(self):
        super().__init__("ToBakery")
    def get_description(self):
        return "Enter the bakery"
    def get_destination(self):
        return 'bakery'
    def get_method(self):
        return "get"

class ToKitchen(Action):
    def __init__(self):
        super().__init__("ToKitchen")
    def get_description(self):
        return "Enter the kitchen"
    def get_destination(self):
        return 'kitchen'
    def get_method(self):
        return "get"


