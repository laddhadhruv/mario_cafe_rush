from core.room import Room
from core.basehandler import BaseHandler

class VictoryRoom(Room):
    
    def __init__(self, room_id):
        Room.__init__(self, room_id)    # do basic initialization for every room
    
    # return description of room.
    def get_description(self):
        return '''
        You collect the treasure and exit from the house.  You have won the game!  Congratulations!
         '''
    
    # return image of room
    def get_image(self):
        return 'victory.jpg'

# define actions for this room
