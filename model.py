"""Models for PUL application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#using Universal Time Log
from flask_login import UserMixin

from werkzeug.security import generate_password_hash,check_password_hash
import os

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri = os.environ.get('DATABASE_URL').replace("://", "ql://", 1), echo=True):
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

    
class General_chat(db.Model):
    """General chat table"""
    __tablename__ = 'chat'

    chatID = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable= False)

    user = db.relationship('User', backref='General_chat')

    def __repr__(self):
        return f'<General_chat chatID:{self.chatID} timestamp:{self.timestamp} userID:{self.userID} message:{self.message} >'

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

    def __repr__(self):
        return f'<NLP id:{self.id} userID={self.userID} chatID={self.chatID} word_count:{self.word_count} polarity:{self.polarity} filtered_words:{self.filtered_words}>'

if __name__ == '__main__':
    # from server import app

    # connect_to_db(app)
    # db.create_all()
    pass








