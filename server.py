"""Server for PUL web app"""

from flask import Flask, render_template, request, redirect, jsonify, request, flash, jsonify
from jinja2 import StrictUndefined
from flask_socketio import SocketIO, emit
from flask_login import LoginManager,current_user,login_user,logout_user, login_required
from flask_session import Session
import os
from datetime import timedelta
import json

from model import *
from forms import *

import crud


app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
#default session time is 31 days for flask so setting it to 30 mins 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


app.jinja_env.undefined = StrictUndefined

#Declaring loginmanager into a var and using it as a decorator to check if user is logged in
login_manager = LoginManager(app)
login_manager.login_message = ""
#Since socket io will branch off after copying the sessions, we need to turn off manage session for flask session works
Session(app)
#create the server with the var socketio
socketio = SocketIO(app, manage_session=False)
#  cookie=None)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():
    """ TO DO """
    count_dict = crud.count_pos_neg()
    #count_dict = {pos: num, neg:num, total:num}
    messages = crud.get_messages()
    pic = crud.get_plant_health(crud.get_ratio(count_dict))
    form = WordsForm()

    return render_template("index.html", messages = messages, count = count_dict, pic = pic, form = form)

@socketio.on('connect')
def connected():
    print('Connected!')

@socketio.on('disconnect')
def diconnected():
    print('Disconnected')

@socketio.on('messaging')
def handle_message(data):
    """ ADD HERE"""
    #Data wil be {username = username, message = userMessage,timestamp = timestamp}
    """Handle the messages coming in, data will be in in json string then used json to make into dictionary"""
    print('new line', data)
    data = json.loads(data)
    #Save the incoming messages into General_chat table
    if data['username']:
        ##TO DO : add to check if the message is valid
        chatID = crud.save_chat_message(data)
        #returns the latest chat id 
        comp_or_neg = crud.save_nlp(data, chatID)
        data['polarity'] = comp_or_neg
        #Adding a new key/value to the data dictionary
    
    emit('new line',data, broadcast=True)

@socketio.on('health')
def handle_plant_health(data):
    # data = {positive : counts.positive.toString(), negative : counts.negative.toString(), total: counts.total.toString()}
    count_dict = crud.get_ratio(data)

    pic = crud.get_plant_health(count_dict)

    emit('my_image', {'plant_pic': "plant_pic", 'pic': pic})


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
            flash('Invalid username or password', 'flash')
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

@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def change_password():
    """Change Password:TO DO ADD DETAILS """
    form = UserprofileForm()
    if form.validate_on_submit():
        username = current_user.username
        user = crud.login_check(username, form.password.data)
        #checking if the current password is right
        if user:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash("New Password Saved!")
        else:
            flash("Wrong credentials")
    elif request.method == "GET":
        #Return back the username into the form 
        form.username.data = current_user.username
    
    return render_template("profile.html", form = form)

@app.route('/getPolarity', methods=["POST"])
def sentiment_form():
    """From the AJAX request from chatt.js, return var answer as a dictionary with the results
    """
    #add a if statment if the text is not empty
    #needed the post listed in method for AJAX request can come through
    form = WordsForm()
    quest = form.data.get('analysis')
    text = form.data.get('text')
    if form.validate_on_submit():
        print('Someone is trying the analyzer!')
        result = crud.print_polarity_from_input(quest,text)
        #if the chosen analysis is "PAT", result would comback as a float else would come out Sentiment class from Naive
        if not isinstance(result, float):
            # ex)Sentiment(classification='pos', p_pos=0.5702702702702702, p_neg=0.4297297297297299)
            answer = crud.break_down_naive(result)
            return jsonify(answer)
        else:
            answer = crud.print_pos_neg(result)
            return jsonify({'class':answer, 'polarity':result})

    return jsonify(data=form.errors)
    #Forms input requriments would be sent out instead


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
    socketio.run(app, host='0.0.0.0', debug=True)