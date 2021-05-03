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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():
    """When the user connects, the database will send over latest inputs to load the html along with the pic appropriate to the plant's health
    The sentiment analyzer form is also returned in the homepage"""
    count_dict = crud.count_pos_neg()
    messages = crud.get_messages()
    pic = crud.get_plant_health(crud.get_ratio(count_dict))
    form = WordsForm()
    return render_template("index.html", messages = messages, count = count_dict, pic = pic, form = form)

##### REAL TIME asynchronous routes ######

@socketio.on('connect')
def connected():
    """Print conncted if any one connects to the website"""
    print('Connected!')

@socketio.on('disconnect')
def diconnected():
    """Print disconnected if any one connects to the website"""
    print('Disconnected')

@socketio.on('messaging')
def handle_message(data):
    """Socket's first real listener event when a user sends a message in chat. 
    So save the user message if the user is active, and return the polarity of 
    the message input along with the time stamp as a string dictionary in data under event called "new line" """
    print('new line', data)
    data = json.loads(data)
    #Save the incoming messages into General_chat table
    if data['username']:
        latest_entry = crud.save_chat_message(data)
        comp_or_neg = crud.save_nlp(data, latest_entry.chatID)
        data['polarity'] = comp_or_neg
        data['timestamp'] = latest_entry.timestamp.strftime('%b-%d-%y %H:%M')
    emit('new line',data, broadcast=True)

@socketio.on('health')
def handle_plant_health(data):
    """ Front end will send back the live chat's pos/neg counts. Server to send back the appropriate pic back to all connected users"""
    count_dict = crud.get_ratio(data)

    pic = crud.get_plant_health(count_dict)

    emit('my_image', {'plant_pic': "plant_pic", 'pic': pic})

#####  USER LOGIN, LOGOUT, EDIT PASSWORD, CHECK MESSAGE SENTIMENT routes ######
def check_if_logged_in():
    """Check if the user was already logged in"""
    if current_user.is_authenticated:
        return redirect("index.html")

@app.route('/login', methods= ['POST', 'GET'])
def login():
    """login with credentials"""
    check_if_logged_in()

    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        username = form.username.data

        password = form.password.data

        user = crud.login_check(username, password)
        #if user is returned then success! 
        if user is None:
            flash('Invalid username or password', 'flash')
            return redirect('/login')        
        
        login_user(user)

        return redirect('/')


    return render_template("login.html", form=form)


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
    """Change Password by checking if hashed passwords matches and return errors or sucess message """
    form = UserprofileForm()
    if form.validate_on_submit():
        username = current_user.username
        user = crud.login_check(username, form.password.data)
        #Checking if the current password is right
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

@app.route('/logout')
def logout():
    """Log out using flask login lib"""
    crud.login_track(current_user.username)
    logout_user()
    return redirect("/")


@app.route('/analyze')
def analyze_page():
    """This page will render different information for current users vs new users"""
    form = WordsForm()
    if current_user.is_authenticated:
        latest_messages = NLP.query.options(db.joinedload(NLP.chat)).filter_by(userID=current_user.id).order_by(NLP.chatID.desc()).limit(5)
        earliest_messages = NLP.query.options(db.joinedload(NLP.chat)).filter_by(userID=current_user.id).order_by(NLP.chatID).limit(5)
        #list of messages selected from DB
        return render_template("analyze.html", latest_messages=latest_messages, earliest_messages=earliest_messages, form=form)
    else:
        all_latest_messages = NLP.query.options(db.joinedload(NLP.chat),db.joinedload(NLP.user)).order_by(NLP.chatID.desc()).limit(5)
        all_earliest_messages = NLP.query.options(db.joinedload(NLP.chat),db.joinedload(NLP.user)).order_by(NLP.chatID).limit(5)
        return render_template("analyze.html", latest_messages=all_latest_messages , earliest_messages=all_earliest_messages, form=form)



##### AJAX CALL HANDLER from Sentiment Analysis form ######

@app.route('/getPolarity', methods=["POST"])
def sentiment_form():
    """From the AJAX request from chatty.js, return var answer as a dictionary with the results
    """
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




if __name__ == '__main__':
    connect_to_db(app)
    
    socketio.run(app, host='0.0.0.0', debug=True)