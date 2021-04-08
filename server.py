"""Server for PUL web app"""

from flask import Flask, render_template, request, flash, redirect, jsonify, request
from jinja2 import StrictUndefined
from flask_socketio import SocketIO, emit
from flask_login import LoginManager
from flask_session import Session

from model import *
from login import *

import crud

app = Flask(__name__)
app.secret_key = "test"
app.config['SESSION_TYPE'] = 'filesystem'

app.jinja_env.undefined = StrictUndefined

#Declaring loginmanager into a var and using it as a decorator to check if user is logged in
login_manager = LoginManager()
#Since socket io will branch off after copying the sessions, we need to turn off manage session for flask session works
Session(app)
#create the server with the var socketio
socketio = SocketIO(app, manage_session=False)



#Checking to see if user is already logged
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    return render_template("homepage.html")

#Flask-SocketIO also dispatches connection and disconnection events
@app.route('/chat')
def testsocket():
    return render_template("testsocket.html")

@socketio.on('connect')
def connected():
    print('Connected!')

@socketio.on('disconnect')
def diconnected():
    print('Disconnected')

# @socketio.on('my event')
# def handle_my_custom_event(data):
#     print('my response', data)
#     print(data['user_name'])
#     emit('my response', data, broadcast=True)
 
@socketio.on('login timestamp')
def log_time(data):
    #from the first connect, I want this to print with the username information 
    print(f"New Connection! {data['user_name']} has joined")
    time_stamps = crud.login_track(data['user_name'])
    emit('my response', data, broadcast=True)
#data is a dictionary     s

@socketio.on('messaging')
def handle_message(data):
    #Data wil be {username = username, message = userMessage,timestamp = timestamp}
    """Handle the messages coming in"""
    # save_message = crud.save_chat_message(fdsfdsfdsfdsafdas)
    emit('my response',data, broadcast=True)




@app.route('/login', methods= ['POST', 'GET'])
def login():
    """login with credentials"""
    form = LoginForm(request.form)

    #WTF built in function will check for my convenience
    #https://flask-wtf.readthedocs.io/en/stable/quickstart.html     
    if form.validate_on_submit():
        username = form.username.data

        password = form.password.data

        user_id = crud.login_check(username, password)
        #if the user_id num is returned then succesffully logged in! 
        if user_id:
            return redirect('/chat')

    return render_template("login.html", form=form)

@app.route('/register', methods=['POST', 'GET'])
def register_user():
    """Create a new user."""
    form = RegisterForm(request.form)


    if form.validate_on_submit():
        username =form.username.data
        print(username)
        password= form.password.data
        print(password)
    
        new_user = crud.create_user(username,password)
        #though create_user function was wrong but not the case... hmmm

        flash('Welcome New User! Please log in')
        return redirect("/login")

    return render_template("register.html", form=form)


#let's run this thing! 

if __name__ == '__main__':
    connect_to_db(app)
    # app.run(port=5000, host='0.0.0.0', debug=True)
    socketio.run(app, host='0.0.0.0', debug=True)