"""Server for PUL web app"""

from flask import Flask, render_template, request, flash, redirect, jsonify
from jinja2 import StrictUndefined
from flask_socketio import SocketIO, send, emit

from model import *

import crud

app = Flask(__name__)
app.secret_key = "test"
app.jinja_env.undefined = StrictUndefined

#create the server using socket 
socketIO = SocketIO(app, cors_allowed_origins="*")

# app.host='localhost'

@app.route('/')
def homepage():
    """Homepage route"""
    return render_template('homepage.html')

@socketIO.on('connect')
def connected():
    print('Connected!')

@socketIO.on('disconnect')
def diconnected():
    print('Disconnected')

@socketIO.on('message')
def handle_message(message):
    print('recived message: ' + message)
    send(message, broadcast=True)


# @socketIO.on('UserAdded')
# def userAdded(message):
#     print('User Added')
#     emit('userAddedResponse'), {'data':message}, broadcast=True)



# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

# @socketIO.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: '+ str(json))
# #     send('my response', json, callback=messageReceived)


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
        flash("Successfully logged in")
    else:
        flash('Wrong credentials. Try again')

    return render_template ('base.html')


#let's run this thing! 

if __name__ == '__main__':
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0', debug=True)
    # socketIO.run(app, debug=False, logger=True, engineio_logger=True)