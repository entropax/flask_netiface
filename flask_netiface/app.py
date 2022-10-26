import random
from datetime import timedelta

from flask import (
     Flask,
     session,
     render_template,
     request,
     redirect,
     url_for,
     flash)
from flask_caching import Cache
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap5
from wtforms.validators import IPAddress


def create_app(test_config=None):
    # create and configure the app with factory
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(minutes=7)
    app.config.from_mapping(
        SECRET_KEY='supersecret',
        SECRET_COOKIE=random.getrandbits(128),
        CACHE_TYPE='SimpleCache'
    )
    cache = Cache(app)
    socketio = SocketIO(app)
    bootstrap = Bootstrap5(app)

    @app.route('/', methods=['GET'])
    def index():
        return 'main page'

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        pass

    @app.route('/switch_state', methods=['POST'])
    def switch_state():
        pass

    @app.route('/add_ip', methods=['POST'])
    def add_ip():
        pass

    @app.route('/del_ip', methods=['POST'])
    def del_ip():
        pass

    @app.route('/change_ip', methods=['POST'])
    def change_ip():
        pass

    @app.route('/change_mask', methods=['POST'])
    def change_mask():
        pass

    @app.route('/logout')
    def logout():
        pass

    @socketio.on('disconnect')
    def disconnect():
        logout()

    return app
