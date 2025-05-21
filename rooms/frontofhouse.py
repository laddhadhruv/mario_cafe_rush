import random
from core.basehandler import BaseHandler
from core.room import Room
from core.action import Action
from core.support import set_cutscene, get_game
from items.orderable_items import Croissant, Bread, Egg, Bacon, Coffee as OrderableCoffee
from items.espresso import Espresso # Keep Espresso for making specific coffee drinks

class FrontOfHouse(Room):
    def __init__(self, room_id):
        Room.__init__(self, room_id)
        self.possible_items = [
            Croissant(filled=False), Croissant(filled=True),
            Bread(toasted=False), Bread(toasted=True),
            Egg(style="scrambled"), Egg(style="boiled"), Egg(style="omelette"),
            Bacon(cooking_style="soft"), Bacon(cooking_style="crispy"),
            OrderableCoffee(coffee_type="espresso"), # ID: "espresso"
            OrderableCoffee(coffee_type="americano_drink"), # ID: "americano_drink"
            OrderableCoffee(coffee_type="cortado_drink"),   # ID: "cortado_drink"
            OrderableCoffee(coffee_type="cappuccino_drink"),# ID: "cappuccino_drink"
            OrderableCoffee(coffee_type="latte_drink")      # ID: "latte_drink"
        ]
        self.current_order = []
        self.orders_completed = 0
        self.orders_to_win = 3 # Adjust as needed

        self.add_action(Out)
        self.add_action(ToBakery)
        self.add_action(ToCoffeeBar)
        self.add_action(ToKitchen)
        self.add_action(RequestNewOrder)
        self.add_action(DeliverOrder)

    def generate_new_order(self):
        if not self.current_order: # Only generate if no active order
            order_size = random.randint(1, 3) # Order between 1 and 3 items
            self.current_order = random.sample(self.possible_items, order_size)
            set_cutscene(f"New order received: {', '.join([item.get_description() for item in self.current_order])}")
        else:
            set_cutscene("Please complete the current order first.")

    def get_description(self):
        desc = "Welcome to Café Byte. Check for new orders or deliver completed ones."
        if self.current_order:
            order_desc = ", ".join([item.get_description() for item in self.current_order])
            desc += f"\nCurrent Order: {order_desc}"
        else:
            desc += "\nNo current order. Click 'Request New Order'."
        desc += f"\nOrders Completed: {self.orders_completed}/{self.orders_to_win}"
        return desc

    def get_image(self):
        return 'entrance_cafe.png'

    def attempt_delivery(self):
        game = get_game()
        player = game.get_player()

        if not self.current_order:
            set_cutscene("There's no active order to deliver.")
            return False

        # Check if all items in current_order are in player's inventory (which are dropped into the room)
        # For simplicity, we check if the player's inventory (items dropped here) matches the order items' descriptions
        
        # Items dropped by the player into this room become part of this room's inventory
        room_inventory_items = [item.get_id() for item in self.inventory.values()]
        order_item_ids = [item.get_id() for item in self.current_order]

        # Check if all required items are present by comparing IDs
        all_items_present = all(o_id in room_inventory_items for o_id in order_item_ids)
        
        # Optional: check if there are no extra items. For now, we only check if required items are present.
        # exact_match = all_items_present and len(room_inventory_items) == len(order_item_ids)


        if all_items_present:
            set_cutscene("Order delivered successfully!")
            self.orders_completed += 1
            self.current_order = [] # Clear current order
            
            # Clear the delivered items from the room's inventory (and thus player's effective drop)
            # This is important so they don't count for the next order
            ids_to_remove = order_item_ids[:] #  Make a copy to iterate and modify
            for item_id_to_remove in ids_to_remove:
                if item_id_to_remove in self.inventory:
                    del self.inventory[item_id_to_remove]
            
            if self.orders_completed >= self.orders_to_win:
                set_cutscene("Congratulations! You've completed all orders and won the game!")
                return 'victory_room' # Return room_id to navigate
            return True # Indicates successful delivery
        else:
            missing_items_desc = []
            present_items_desc = [self.inventory[item_id].get_description() for item_id in room_inventory_items if item_id in self.inventory] # Descriptions of items in room
            
            for order_item in self.current_order:
                if order_item.get_id() not in room_inventory_items:
                    missing_items_desc.append(order_item.get_description())
            
            cutscene_message = "Order not complete. "
            if missing_items_desc:
                cutscene_message += f"Missing: {', '.join(missing_items_desc)}. "
            if present_items_desc:
                 cutscene_message += f"You have: {', '.join(present_items_desc)}."
            else:
                cutscene_message += "You haven't presented any items for the order."

            set_cutscene(cutscene_message)
            return False

# define actions for this room

class RequestNewOrder(Action):
    def __init__(self):
        Action.__init__(self, "RequestNewOrder")
    
    def get_description(self):
        return "Request New Order"
    
    def get_method(self):
        return "post" # Modifies room state (current_order)

    def is_enabled(self):
        # Enable only if there is no current order
        return not self.room.current_order

    def do_action(self, game, room, request):
        room.generate_new_order()
        return

class DeliverOrder(Action):
    def __init__(self):
        Action.__init__(self, "DeliverOrder")
    
    def get_description(self):
        return "Deliver Current Order"

    def get_method(self):
        return "post" # Modifies room state (orders_completed, current_order)

    def is_enabled(self):
        # Enable only if there is a current order and player is in frontofhouse
        return self.room.current_order and get_game().get_current_room().id == 'frontofhouse'

    def do_action(self, game, room, request):
        # The actual delivery logic is now inside the room's attempt_delivery method
        # because the "Drop Item" action in basehandler.py handles moving items to room inventory
        # We just need to trigger the check here.
        # No, the "drop item" action is a separate POST request.
        # This "DeliverOrder" action should itself perform the check based on items already dropped (i.e. in room inventory)
        
        destination_room_id = room.attempt_delivery()
        if destination_room_id == 'victory_room': # Check if attempt_delivery signals a win
             game.set_current_room('victory_room') # Manually change room
        # No explicit return needed to stay in the same room unless changing rooms

class Out(Action):
    def __init__(self):
        Action.__init__(self, "Out")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Go Outside"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'startingpoint'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"

class ToBakery(Action):
    def __init__(self):
        Action.__init__(self, "ToBakery")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter the bakery"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'bakery'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
class ToKitchen(Action):
    def __init__(self):
        Action.__init__(self, "ToKitchen")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter the kitchen"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'kitchen'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
class ToCoffeeBar(Action):
    def __init__(self):
        Action.__init__(self, "ToCoffeeBar")    # do basic initialization for every action
    
    # return description of action (used in label on webpage)
    def get_description(self):
        return "Enter the coffee bar"
    
    # return id of room to enter when action is complete
    def get_destination(self):
        return 'coffeebar'
    
    # return http method to use when user clicks on this action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    def get_method(self):
        return "get"
    
# order: a list, set or dictionary; potentially order; container to self.order in this room; find condition for how it's set -> next order button
# random number generator w/ ID #s for items; keys are IDs and items are descriptions
# multiples of items e.g. coffee2, espresso3, etc.
# function to look up given ID with state
# display order -> either room gets custom template or global template
# deliver order = reset state of items to original location
# best idea: container for order; set number of orders to win the game, completed orders counts toward 1
# victory state = separate room