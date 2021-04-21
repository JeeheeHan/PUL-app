"""Server for PUL web app"""

from flask import Flask, render_template, request, redirect, jsonify, request, flash
from jinja2 import StrictUndefined
from flask_socketio import SocketIO, emit
from flask_login import LoginManager,current_user,login_user,logout_user
from flask_session import Session

from model import *
from login import *

import crud

app = Flask(__name__)

app.secret_key = "test"
app.config['SESSION_TYPE'] = 'filesystem'

app.jinja_env.undefined = StrictUndefined

#Declaring loginmanager into a var and using it as a decorator to check if user is logged in
login_manager = LoginManager(app)
#Since socket io will branch off after copying the sessions, we need to turn off manage session for flask session works
Session(app)
#create the server with the var socketio
socketio = SocketIO(app, manage_session=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    messages = crud.get_messages()
    return render_template("index.html", messages = messages)

#Flask-SocketIO also dispatches connection and disconnection events
@app.route('/chat')
def testsocket():
    return render_template("public.html")

@socketio.on('connect')
def connected():
    print('Connected!')

@socketio.on('disconnect')
def diconnected():
    print('Disconnected')

@socketio.on('messaging')
def handle_message(data):
    #Data wil be {username = username, message = userMessage,timestamp = timestamp}
    """Handle the messages coming in"""
    print('new line', data)
    #Save the incoming messages into General_chat table
    if data['username']:
        chatID = crud.save_chat_message(data)
        #returns the latest chat id 
        comp_or_neg = crud.save_nlp(data, chatID)
        data['polarity'] = comp_or_neg
        #Adding a new key/value to the data dictionary
    emit('new line',data, broadcast=True)



#Wait for front end to call for plant call 
@app.route('/plantCall')
def send_sentiment():
    """Emit the latest sentiment num"""
    num = crud.get_sentiment()
    # socketio.emit('sentiment', str(num))
    return str(num)

def check_if_logged_in():
    """Check if the user was already logged in"""
    if current_user.is_authenticated:
        return redirect("index.html")

@app.route('/login', methods= ['POST', 'GET'])
def login():
    """login with credentials"""
    check_if_logged_in()

    form = LoginForm(request.form)

    #WTF built in function will check for my convenience
    #https://flask-wtf.readthedocs.io/en/stable/quickstart.html     
    if form.validate_on_submit():
        username = form.username.data

        password = form.password.data

        user = crud.login_check(username, password)
        #if user is returned then success! 
        if user is None:
            flash('Invalid username or password')
            return redirect('/login')        
 

        crud.login_track(user.username)
        login_user(user)

        return redirect('/')


    return render_template("login.html", form=form)
    # pass in the most recent sentiment and have plant status to change using jinja

@app.route('/register', methods=['POST', 'GET'])
def register_user():
    """Create a new user."""
    check_if_logged_in()

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        username =form.username.data
        password= form.password.data
        new_user = crud.create_user(username,password)

        return redirect("/login")

    return render_template("register.html", form=form)

@app.route('/logout')
def logout():
    """Log out using flask login lib"""
    logout_user()
    return redirect("/")


@app.route('/words')
def all_words():
    """Just print all the words on there"""
    words = crud.get_words()
    return render_template("plant.html", words=words)

#let's run this thing! 

if __name__ == '__main__':
    connect_to_db(app)
    # app.run(port=5000, host='0.0.0.0', debug=True)
    socketio.run(app, host='0.0.0.0', debug=True)