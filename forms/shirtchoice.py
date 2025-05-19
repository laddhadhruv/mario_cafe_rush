from flask import Flask, request
from core.form import FormHandler
from core.support import set_cutscene

class ShirtChoiceHandler(FormHandler):

    def __init__(self, app:Flask, form_id:str, template:str):
        super().__init__(app, form_id, template)

    # Get Methods
    #############

    def update_parameters(self, request, game, parameters):
        parameters['has_keys'] = 'Putting on a shirt is hard while holding keys' if 'keys' in game.get_player().inventory else ""
        return parameters

    # Post Methods
    ##############
    
    def update_game(self, request, game):
        set_cutscene('You are now wearing the ' + request.form['shirt'] + " shirt.")
    
    def get_destination(self, request, game):
        return 'closet'
