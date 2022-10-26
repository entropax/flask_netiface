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

from flask_netiface.auth import sudo_perm_validator
from flask_netiface.net_interface import (
    get_interfaces_info,
    add_ip_address,
    delete_ip_address,
    change_ip_address,
    change_ip_mask,
    switch_interface_status)


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
        return render_template('index.html', interfaces=get_interfaces_info())

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        if request.method == 'POST':
            password = request.form['password']
            if sudo_perm_validator(password):
                cache.set('password', password)
                session.permanent = False
                session['key'] = app.config['SECRET_COOKIE']
                return redirect(url_for('index'))
            else:
                return render_template('auth.html', password='False')

        return render_template('auth.html')

    @app.route('/switch_state', methods=['POST'])
    def switch_state():
        interfaces = get_interfaces_info()
        interface_button = list(request.form.keys())[0]
        if interface_button in interfaces:
            interface_name = interface_button
            interface_status = interfaces[interface_name]['state']
            switch_interface_status(
                    interface_name,
                    interface_status,
                    cache.get('password'))
            interfaces = get_interfaces_info()
            return redirect(url_for('index'))
        return redirect(url_for('index'))

    @app.route('/add_ip', methods=['POST'])
    def add_ip():
        interface_name = list(request.form.keys())[0]
        ip_address = request.form.get(interface_name)
        validator = IPAddress()
        if validator.check_ipv4(ip_address):
            add_ip_address(
                interface_name,
                ip_address,
                cache.get('password'))
            return redirect(url_for('index'))
        flash('ip address or mask was incorrect')
        return redirect(url_for('index'))

    @app.route('/del_ip', methods=['POST'])
    def del_ip():
        ip_address = list(request.form.keys())[0]
        interface_name = list(request.form.keys())[1]
        delete_ip_address(
            interface_name,
            ip_address,
            cache.get('password'))
        return redirect(url_for('index'))

    @app.route('/change_ip', methods=['POST'])
    def change_ip():
        interface_name = list(request.form.keys())[1]
        new_ip = request.form.get(interface_name)
        old_ip = list(request.form.keys())[0]
        validator = IPAddress()
        if validator.check_ipv4(new_ip):
            change_ip_address(
                interface_name,
                new_ip,
                old_ip,
                cache.get('password'))
            return redirect(url_for('index'))
        return redirect(url_for('index'))

    @app.route('/change_mask', methods=['POST'])
    def change_mask():
        print(request.form)
        print(request.form.keys())
        interface_name = list(request.form.keys())[2]
        ip_address = list(request.form.keys())[1]
        new_mask = request.form.get(interface_name)
        validator = IPAddress()
        if validator.check_ipv4(new_mask):
            change_ip_mask(
                    interface_name,
                    ip_address,
                    new_mask,
                    cache.get('password'))
            return redirect(url_for('index'))
        flash('ip address or mask was incorrect')
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        cache.set('password', None)
        session['key'] = None
        return redirect(url_for('index'))

    @socketio.on('disconnect')
    def disconnect():
        logout()

    return app
