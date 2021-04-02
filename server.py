"""Server for PUL web app"""

from flask import Flask, render_template, request, flash, session, redirect
from jinja2 import StrictUndefined
from flask_socketio import SocketIO, send, emit

import eventlet
import gevent

import crud

app = Flask(__name__)
app.secret_key = "test"

#create the server using socket 
socketIO = SocketIO(app, cors_allowed_origins="*")

# app.host='localhost'

@app.route('/')
def homepage():
    """Homepage route"""
    return render_template('homepage.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketIO.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    send('my response', json, callback=messageReceived)

@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

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
        flash('Logged in!')
    else:
        flash('Wrong credentials. Try again')

    return redirect ('/')



#let's run this thing! 

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
    socketIO.run(app, debug=False, logger=True, engineio_logger=True)