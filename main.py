import os
import json
import csv
from datetime import datetime

from flask import (
    Flask, redirect, render_template, request,
    session, url_for
)
from flask_session import Session

from core.support import registerHandler, registerForm, reset_game
from rooms.startingpoint import StartingPoint
from rooms.frontofhouse import FrontOfHouse
from rooms.kitchen import Kitchen
from rooms.bakery import Bakery
from rooms.coffeebar import CoffeeBar
from forms.shirtchoice import ShirtChoiceHandler
from rooms.victory_room import VictoryRoom

# ─── Constants ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
HOF_PATH    = os.path.join(BASE_DIR, 'hall_of_fame.csv')
# ──────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = b'787c5ff49ec3c651ea1dee62118a35b37bb3ec843f2bfbac59fce44c10d85158'
app.config['SESSION_TYPE'] = 'filesystem'

# ─── Load JSON config into Flask’s config ────────────────────────────────────
with open(CONFIG_PATH, 'r') as f:
    app.config.update(json.load(f))
# ──────────────────────────────────────────────────────────────────────────────

# ─── Context processor to expose config in all templates ─────────────────────
@app.context_processor
def inject_config():
    return {
      'config': app.config,
      'game_start': session.get('game_start')
    }
# ──────────────────────────────────────────────────────────────────────────────

# ─── SETTINGS ROUTES ─────────────────────────────────────────────────────────
@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html', config=app.config)

@app.route('/settings', methods=['POST'])
def settings_post():
    with open(CONFIG_PATH, 'r') as f:
        cfg = json.load(f)

    form = request.form
    def parse_int(field, current):
        val = form.get(field, '').strip()
        return int(val) if val.isdigit() else current

    cfg['orders_to_win'] = parse_int('orders_to_win', cfg.get('orders_to_win', 3))
    cfg.setdefault('order_size', {})
    cfg['order_size']['min'] = parse_int('order_size_min', cfg['order_size'].get('min', 1))
    cfg['order_size']['max'] = parse_int('order_size_max', cfg['order_size'].get('max', 3))
    cfg['time_limit'] = parse_int('time_limit', cfg.get('time_limit', 30))
    player_name = form.get('player_name', '').strip()
    if player_name:
        cfg['player_name'] = player_name

    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f, indent=2)

    app.config.update(cfg)
    return redirect('/frontofhouse')
# ──────────────────────────────────────────────────────────────────────────────

# ─── Initialize Flask‐Session ─────────────────────────────────────────────────
if __name__ != '__main__':
    app.config['SESSION_FILE_DIR'] = '/tmp'
Session().init_app(app)
# ──────────────────────────────────────────────────────────────────────────────

# ─── CORE GAME ROUTES ────────────────────────────────────────────────────────
@app.route('/restart')
def restart():
    reset_game()
    return redirect('/')

@app.route('/')
def defaultstart():
    return redirect('/startingpoint')

@app.route('/startingpoint', methods=['GET', 'POST'])
def startingpoint():
    return registerHandler(app, StartingPoint, 'startingpoint').update()

@app.route('/lose')
def lose():

    class DummyRoom: id = 'lose'
    return render_template('lose.html', room=DummyRoom())

@app.route('/frontofhouse', methods=['GET','POST'])
def frontofhouse():
    if 'game_start' not in session:
        session['game_start'] = datetime.utcnow().isoformat()
    # now render as normal—timerInitialized will get set in the template
    return registerHandler(app, FrontOfHouse, 'frontofhouse').update()

@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    return registerHandler(app, Kitchen, 'kitchen').update()

@app.route('/bakery', methods=['GET', 'POST'])
def bakery():
    return registerHandler(app, Bakery, 'bakery').update()

@app.route('/coffeebar', methods=['GET', 'POST'])
def coffeebar():
    return registerHandler(app, CoffeeBar, 'coffeebar').update()

@app.route('/shirtchoice', methods=['GET', 'POST'])
def shirtchoice():
    return registerForm(
        app,
        'shirtchoice',
        'shirtchoice.html',
        ShirtChoiceHandler
    ).update()
# ──────────────────────────────────────────────────────────────────────────────

# ─── VICTORY & CSV LOGGING ───────────────────────────────────────────────────
@app.route('/victory_room', methods=['GET', 'POST'])
def victory_room():
    # log the win into hall_of_fame.csv
    from core.support import get_game
    game   = get_game()
    player = game.get_player()

    gs_iso = session.get('game_start')
    starts = session.get('order_starts', [])
    ends   = session.get('order_ends', [])

    if gs_iso and starts and ends:
        gs = datetime.fromisoformat(gs_iso)
        order_ts = [datetime.fromisoformat(t) for t in starts]
        order_te = [datetime.fromisoformat(t) for t in ends]

        total_time = (order_te[-1] - gs).total_seconds()
        order_durations = [
            (te - ts).total_seconds()
            for ts, te in zip(order_ts, order_te)
        ]
        item_times = [
            round(d / app.config['order_size']['max'], 3)
            for d in order_durations
        ]

        row = {
            'timestamp':    gs.isoformat(),
            'player_name':  player.name,
            'orders_to_win':app.config['orders_to_win'],
            'order_min':    app.config['order_size']['min'],
            'order_max':    app.config['order_size']['max'],
            'time_limit':   app.config['time_limit'],
            'total_time':   total_time,
            'order_durations': '|'.join(str(d) for d in order_durations),
            'item_times':      '|'.join(str(t) for t in item_times)
        }

        new_file = not os.path.exists(HOF_PATH)
        with open(HOF_PATH, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            if new_file:
                writer.writeheader()
            writer.writerow(row)

    # clear out the timing session keys
    for k in ('game_start', 'order_starts', 'order_ends'):
        session.pop(k, None)

    return registerHandler(app, VictoryRoom, 'victory_room').update()
# ──────────────────────────────────────────────────────────────────────────────

# ─── HALL OF FAME ROUTE ──────────────────────────────────────────────────────
@app.route('/halloffame')
def halloffame():
    if not os.path.exists(HOF_PATH):
        entries = []
    else:
        with open(HOF_PATH, newline='') as csvfile:
            entries = list(csv.DictReader(csvfile))
    return render_template('halloffame.html', entries=entries)
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
