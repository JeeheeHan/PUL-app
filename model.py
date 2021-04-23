"""Models for PUL application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#using Universal Time Log
from flask_login import UserMixin

from werkzeug.security import generate_password_hash,check_password_hash


db = SQLAlchemy()

def connect_to_db(flask_app, db_uri = 'postgresql:///pul_db', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connect to DB!')


class User(UserMixin, db.Model):
    #to be able to call the 4 methods from flask Login mod
    """ A user table class"""
    __tablename__ ='users'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(24), unique=True)
    password = db.Column(db.String, nullable= False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def set_password(self, password):
        """Hash out the passwords"""
        self.password = generate_password_hash(password)
    def check_password(self, pwd):
        """Match passwords"""
        return check_password_hash(self.password, pwd)


    def __repr__(self):
        return f'<Username:{self.username}>'

#remember to add the repr
class Adjectives(db.Model):
    """ALL the list of words combined"""

    __tablename__ = 'words'

    adj_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    word_type = db.Column(db.Integer)
    #keeping the type to be an integer for now so maybe i can call it earlier 
    word = db.Column(db.String)

class General_chat(db.Model):
    """General chat table"""
    __tablename__ = 'chat'

    chatID = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #review this later in case of message time stamp thing 
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable= False)

    user = db.relationship('User', backref='General_chat')

class NLP(db.Model):
    """NLP table"""
    __tablename__ = 'nlp'

    id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    chatID = db.Column(db.Integer, db.ForeignKey('chat.chatID'))
    word_count = db.Column(db.Integer)
    polarity = db.Column(db.Float)
    filtered_words = db.Column(db.Text)
    #going to string the words
    
    user = db.relationship('User', backref='NLP')
    chat = db.relationship('General_chat', backref='NLP')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    db.create_all()








