from core.room import Room
from core.action import Action

class VictoryRoom(Room):
    
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
        self.add_action(RestartGameAction)
    
    def get_template(self):
        # point explicitly at your custom template
        return 'victory_room.html'
    
    # return description of room.
    def get_description(self):
        return '''
        Congratulations! You've successfully served all the rushed customers 
        and completed all orders for the day. You are a true Café Byte champion!
        '''
    
    # return image of room
    def get_image(self):
        return 'victory.jpg'

# Define RestartGameAction
class RestartGameAction(Action):
    def __init__(self):
        super().__init__("RestartGame") # Action ID
    
    def get_description(self):
        return "Restart Game"
    
    def get_method(self):
        return "get" 

    def is_nav_action(self):
        return True

    def get_destination(self):
        return "restart" # Will be prefixed with / by core.support.get_path()

    def do_action(self, game, room, request):
        # The reset_game() is called by the /restart endpoint handler in main.py.
        # This action only needs to navigate there.
        pass

# define actions for this room
