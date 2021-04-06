"""Server for PUL web app"""

from flask import Flask, render_template, request, flash, redirect, jsonify
from jinja2 import StrictUndefined
from flask_socketio import SocketIO, emit

from model import *

import crud

app = Flask(__name__)
app.secret_key = "test"
app.jinja_env.undefined = StrictUndefined

socketio = SocketIO(app)

#create the server using socket 
# socketIO = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def homepage():
    """Homepage route"""
    return render_template('testsocket.html')

@socketio.on('connect')
def connected():
    print('Connected!')

@socketio.on('disconnect')
def diconnected():
    print('Disconnected')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('my event')
def handle_my_custom_event(data):
    print('my response', data)
    emit('my response', data, broadcast=True)



@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
#revisit the flash message since this won't render to the socket-io
    if user:
        flash("Account with this email exists")
    else:
        crud.create_user(email,password)
        flash("Account created! Please log in")

    return redirect('/')

@app.route('/login', methods= ['POST'])
def login():
    """login with credentials"""

    email = request.form.get('email')
    password = request.form.get('password')

    user_id = crud.login_check(email, password)

    if user_id: 
        flash("Successfully logged in")
    else:
        flash('Wrong credentials. Try again')

    return render_template ('base.html')


#let's run this thing! 

if __name__ == '__main__':
    connect_to_db(app)
    # app.run(port=5000, host='0.0.0.0', debug=True)
    socketio.run(app, host='0.0.0.0', debug=True)