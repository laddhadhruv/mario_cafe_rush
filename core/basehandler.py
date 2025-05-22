from flask import Flask, request, render_template, redirect
import core.support
from core.menu import Menu
from core.item import Item
import copy # Import the copy module

class BaseHandler():
    
    def __init__(self, app:Flask, room_class:type, room_id:str, template:str="room.html"):
        self.app = app
        self.room_class = room_class
        self.room_id = room_id
        self.template = template

    def get_template(self):
        return self.template
    
    # handles both get and post requests
    def update(self):
        # get game object, which holds the current state of the game
        self.game = core.support.get_game()        
        this_room = self.get_this_room()
        player = self.game.get_player()
        
        # add the new room to the game history
        self.game.update_history(this_room)
        
        # build menu for room and player
        menu = Menu()
        menu.build_menu(this_room, player)
        
        # if user clicked on an action button we let the
        # corresponding action object update the game state
        # and then redirect to action's destination if it has one
        # or else back to this page
        args = {} # Get args regardless of get or put
        args.update(request.args)
        args.update(request.form)
        if "action_name" in args:
            action_name = args["action_name"]
            action = menu.actions.get(action_name)
            if action:
                action.do_action(self.game,this_room,request)
                self.game.update()
                if action.is_nav_action():
                    return redirect(core.support.get_path(action.get_destination()))
                else:
                    return redirect(request.path)
        
        # if we reach this point in the code, user did not click on an action
        # or the action object couldn't be found (hopefully that doesn't happen)
        # next step is to update inventory if requested
        if 'inventory' in request.form:
            self.update_inventory(this_room,player)
            
        # final step is to render the page for the current room (if this is a get)
        if request.method == 'GET':
            web_page_parameters = {
               "this_page":request.path,
               "room":this_room,
               "menu":menu,
               "player":player,
               "cutscene":core.support.play_cutscene(),
            }
            return render_template(self.get_template(), **web_page_parameters)
        # otherwise this is a post and we need to redirect back to this page (as get)
        elif request.method=='POST':
            return redirect(request.path)
        else:
            raise Exception(f'Unkown request method: {request.method}')
    
    def get_this_room(self):
        return self.game.get_or_create_room(self.room_id,self.room_class)        

    # update player and room inventories (called from past handler for each room)
    def update_inventory(self,room,player):
        # get name of items that user checked
        add_stuff = request.form.getlist("room_inventory")
        drop_stuff = request.form.getlist("player_inventory")
        
        # note:  in what follows we remove item first, so we get an object
        # and then we add that object to the other list
        
        # if user picked something up, then update player and room inventory
        if add_stuff:
            for item_name in add_stuff:
                # First, get a reference to the item in the room
                original_item_in_room = room.get_item(item_name) 
                
                if isinstance(original_item_in_room, Item):
                    item_to_add_to_player = None
                    if original_item_in_room.is_generator:
                        # If it's a generator, copy it
                        item_to_add_to_player = copy.deepcopy(original_item_in_room)
                        # Reset any state on the copy if necessary, e.g., if it's a coffee machine that produces a fresh espresso
                        # This might require a specific reset method on the Item or its subclasses
                        if hasattr(item_to_add_to_player, 'reset_to_default_state'): # Example method
                            item_to_add_to_player.reset_to_default_state()
                    else:
                        # If not a generator, pop it from the room
                        item_to_add_to_player = room.pop_item(item_name)
                    
                    if isinstance(item_to_add_to_player, Item):
                        item_to_add_to_player.do_item_added(self.game,room,request) # Call on the item being added
                        player.add_item(item_to_add_to_player)
                # else: original_item_in_room was not found or not an Item instance - do nothing or log error
            self.game.update()
        
        # if user dropped something, then update player and room inventory
        if drop_stuff:
            for item_name in drop_stuff:
                item = player.pop_item(item_name)
                if isinstance(item, Item):
                    item.do_item_dropped(self.game,room,request)
                    room.add_item(item)
                # else: item was not found, or pop_item returned default string - do nothing or log error
            self.game.update()
