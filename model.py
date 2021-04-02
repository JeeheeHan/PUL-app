"""Models for PUL application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_to_db(flask_app, db_uri = 'postgresql:///pul_db', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connect to DB!')

class User(db.Model):
    """ A user table class"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String, 
                        unique=True)
    password = db.Column(db.String, nullable= False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f'<User user_id:{self.username}>'

    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = password



class Plants_type(db.Model):
    """Table with different plant types"""

    __tablename__= 'plants_type'

    plant_typeID = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    plant_type = db.Column(db.String, unique=True, nullable=False)
    plant_name = db.Column(db.String)

    def __repr__(self):
        return f'<Plant:{self.plant_name}>'

class Health(db.Model):
    """Health stages for plant"""

    __tablename__= 'health'

    plantID = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    health_status = db.Column(db.String)
    #this would most likely be changed based on the counts of compliments or insults

    plant = db.relationship('Plants_type', backref='health')



class General_chat(db.Model):
    """General chat table"""
    __tablename__ = 'chat'

    chatID = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    #review this later in case of message time stamp thing 
    userID = db.Column(db.Integer, nullable= False)
    message = db.Column(db.String, nullable= False)

    user = db.relationship('User', backref='General_chat')



if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)








