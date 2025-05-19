from flask import Flask, redirect
from flask_session import Session
from core.support import registerHandler, registerForm, reset_game
from rooms.startingpoint import StartingPoint
from rooms.entrancehall import EntranceHall
from rooms.basement import Basement
from rooms.closet import Closet
from forms.shirtchoice import ShirtChoiceHandler
from rooms.treasure_room import TreasureRoom
from rooms.victory_room import VictoryRoom

#Initialize the Flask app and session:
app = Flask(__name__)
app.secret_key = b'787c5ff49ec3c651ea1dee62118a35b37bb3ec843f2bfbac59fce44c10d85158'
app.config['SESSION_TYPE'] = 'filesystem'
if __name__ != '__main__':
    #If running on GAE Cloud
    print("==> Running on GOE and storing sessions to /tmp ramdisk")
    app.config['SESSION_FILE_DIR'] = '/tmp'
Session().init_app(app)

# Configure the restart operation
@app.route('/restart')
def restart():
    reset_game()
    return redirect('/')

# Configure the default location to go to the starting point:
@app.route('/')
def defaultstart():
    return redirect('/startingpoint')

@app.route('/startingpoint', methods=['GET','POST'])
def startingpoint():
    return registerHandler(app, StartingPoint, 'startingpoint').update()

@app.route('/entrancehall', methods=['GET','POST'])
def entrancehall():
    return registerHandler(app, EntranceHall, 'entrancehall').update()

@app.route('/basement', methods=['GET','POST'])
def basement():
    return registerHandler(app, Basement, 'basement').update()

@app.route('/closet', methods=['GET', 'POST'])
def closet():
    return registerHandler(app, Closet, 'closet').update()

@app.route('/shirtchoice', methods=['GET', 'POST'])
def shirtchoice():
    return registerForm(app, 'shirtchoice', 'shirtchoice.html', ShirtChoiceHandler).update()

@app.route('/treasure_room', methods=['GET', 'POST'])
def treasure_room():
    return registerHandler(app, TreasureRoom, 'treasure_room').update()

@app.route('/victory_room', methods=['GET', 'POST'])
def victory_room():
    return registerHandler(app, VictoryRoom, 'victory_room').update()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    