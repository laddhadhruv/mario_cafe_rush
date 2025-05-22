import random
from flask import current_app
from core.basehandler import BaseHandler
from core.room import Room
from core.action import Action
from core.support import set_cutscene, get_game
from items.orderable_items import Croissant, Bread, Egg, Bacon, Coffee as OrderableCoffee
from items.espresso import Espresso
from rooms.victory_room import VictoryRoom
from core.action import DropItem
from flask import session, current_app
from datetime import datetime
from flask import session
from datetime import datetime


class RequestNewOrder(Action):
    def __init__(self):
        super().__init__("RequestNewOrder")
    def get_description(self):
        return "Request New Order"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return not self.room.current_order
    def do_action(self, game, room, request):
        room.generate_new_order()

class DeliverOrder(Action):
    def __init__(self):
        super().__init__("DeliverOrder")
        self.destination_room_id = None
    def get_description(self):
        return "Deliver Current Order"
    def get_method(self):
        return "post"
    def is_enabled(self):
        return self.room.current_order and get_game().get_current_room().id == 'frontofhouse'
    def do_action(self, game, room, request):
        result = room.attempt_delivery()
        self.destination_room_id = None
        if result == 'victory_room':
            vr = game.get_or_create_room('victory_room', VictoryRoom)
            game.update_history(vr)
            self.destination_room_id = 'victory_room'
    def is_nav_action(self):
        return self.destination_room_id is not None
    def get_destination(self):
        return self.destination_room_id

class Out(Action):
    def __init__(self):
        super().__init__("Out")
    def get_description(self):
        return "Go Outside"
    def get_destination(self):
        return 'startingpoint'
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

class ToCoffeeBar(Action):
    def __init__(self):
        super().__init__("ToCoffeeBar")
    def get_description(self):
        return "Enter the coffee bar"
    def get_destination(self):
        return 'coffeebar'
    def get_method(self):
        return "get"

class FrontOfHouse(Room):
    def __init__(self, room_id):
        super().__init__(room_id)

        # ─── pull settings from config.json via app.config ─────────────
        cfg = current_app.config
        if session.get('game_start') is None:
            session['game_start'] = datetime.utcnow().isoformat()
            session['order_starts'] = []
            session['order_ends']   = []
        self.orders_to_win = cfg.get('orders_to_win', 3)
        size_cfg = cfg.get('order_size', {})
        self.order_min   = size_cfg.get('min', 1)
        self.order_max   = size_cfg.get('max', 3)
        # ─────────────────────────────────────────────────────────────

        self.current_order    = []
        self.orders_completed = 0

        # allowed actions
        self.add_action(DropItem)
        self.add_action(RequestNewOrder)
        self.add_action(DeliverOrder)
        self.add_action(Out)
        self.add_action(ToBakery)
        self.add_action(ToCoffeeBar)
        self.add_action(ToKitchen)

        # possible items
        self.possible_items = [
            Croissant(filled=False), Croissant(filled=True),
            Bread(toasted=False),    Bread(toasted=True),
            Egg(style="scrambled"),  Egg(style="boiled"),  Egg(style="omelette"),
            Bacon(cooking_style="soft"), Bacon(cooking_style="crispy"),
            OrderableCoffee(coffee_type="espresso"),
            OrderableCoffee(coffee_type="americano"),
            OrderableCoffee(coffee_type="cortado"),
            OrderableCoffee(coffee_type="cappuccino"),
            OrderableCoffee(coffee_type="latte")
        ]

    def generate_new_order(self):
        # ─── SAFETY NET: initialize timing lists if missing ─────────────────────
        if 'order_starts' not in session:
            session['order_starts'] = []
        if 'order_ends' not in session:
            session['order_ends'] = []
        session.modified = True

        # ─── only generate if no active order ───────────────────────────────────
        if not self.current_order:
            # record order start timestamp
            session['order_starts'].append(datetime.utcnow().isoformat())
            session.modified = True

            # pick a random order size in your configured range
            order_size = random.randint(self.order_min, self.order_max)
            # sample items
            self.current_order = random.sample(self.possible_items, order_size)

            set_cutscene(
                "New order received: "
                + ", ".join(i.get_description() for i in self.current_order)
            )
        else:
            set_cutscene("Please complete the current order first.")

    def get_description(self):
        desc = "Welcome to Café Byte. Check for new orders or deliver completed ones."
        if self.current_order:
            desc += "\nCurrent Order: " + ", ".join(i.get_description() for i in self.current_order)
        else:
            desc += "\nNo current order. Click 'Request New Order'."
        desc += f"\nOrders Completed: {self.orders_completed}/{self.orders_to_win}"
        return desc

    def get_image(self):
        return 'entrance_cafe.png'

    def attempt_delivery(self):
        game   = get_game()
        player = game.get_player()

        if not self.current_order:
            set_cutscene("There's no active order to deliver.")
            return False

        inv_ids   = [i.get_id() for i in player.inventory.values()]
        order_ids = [i.get_id() for i in self.current_order]
        match_all = all(o in inv_ids for o in order_ids) and len(inv_ids) == len(order_ids)

        if match_all:
            session['order_ends'].append(datetime.utcnow().isoformat())
            session.modified = True
            set_cutscene("Order delivered successfully!")
            self.orders_completed += 1
            self.current_order = []
            player.inventory = {}
            game.update()
            if self.orders_completed >= self.orders_to_win:
                set_cutscene("Congratulations! You've completed all orders and won the game!")
                return 'victory_room'
            return True

        # build missing items list
        missing = [
            item.get_description()
            for item in self.current_order
            if item.get_id() not in inv_ids
        ]

        # build extra items list safely by iterating inventory items
        extra = [
            item.get_description()
            for item_id, item in player.inventory.items()
            if item_id not in order_ids
        ]

        # compose the cutscene message
        msg = "Order not complete. "
        if missing:
            msg += "Missing: " + ", ".join(missing) + ". "
        if extra:
            msg += "You presented extra items: " + ", ".join(extra) + ". "
        set_cutscene(msg.strip())

        return False
