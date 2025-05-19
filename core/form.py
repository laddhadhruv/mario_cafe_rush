from flask import Flask, request, render_template, redirect
from core.support import get_game
import logging

class FormHandler():    

    def __init__(self, app:Flask, form_id:str, template:str):
        self.app = app
        self.form_id = form_id
        self.template = template

    def get_template(self, request, game):
        return self.template
    
    # Get Abstract methods
    ######################

    def update_parameters(self, request, game, parameters):
        return parameters

    # Post Abstract methods
    #######################
    
    def update_game(self, request, game):
        pass
    
    def get_destination(self, request, game):
        pass

    # Implemented Methods
    #####################
    
    def update(self):
        if request.method == 'GET':
            return self.get()
        elif request.method=='POST':
            return self.post()
        else:
            raise Exception(f'Unkown request method: {request.method}')

    def get(self):
        logging.info('Form Called')
        game = get_game()
        template = self.get_template(request, game)
        web_page_parameters = {
           "this_page":request.path,
           "game":game,
        }
        web_page_parameters = self.update_parameters(request, game, web_page_parameters)
        return render_template(template, **web_page_parameters)
    
    def post(self):
        game = get_game()
        self.update_game(request, game)
        game.update()
        destination = self.get_destination(request, game)
        return redirect(destination)
        