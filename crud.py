"""Create, read, update and delete"""

from model import *

def create_user(user, pwd):
    """Create and return a new user."""

    user = User(username=user, password=pwd)

    db.session.add(user)
    db.session.commit()

    return user

def login_check(username, password):
    """Check if email matches password"""

    #https://wtforms.readthedocs.io/en/2.3.x/fields/
    try: 
        user = User.query.filter_by(username=username).first()
        password_by_username = user.password

        if password == password_by_username:
            return user.username
    except:
        pass
        # raise ValidationError("Wrong credentials, please try again")

def save_chat_message(data):
    """Saving chat message into DB"""
    username = data['username']
    user_id = User.query.filter_by(username=username).first().user_id
    message = data['message']
    timestamp = data['timestamp']

    db.session.add(General_chat(message=message, userID=user_id, timestamp=timestamp))
    db.session.commit()
    

def login_track(username):
    """Saving last logged into DB"""
    user = User.query.filter_by(username=username).first()
    user.last_login = datetime.utcnow
    return user.last_login
    
def create_adjectives(word_type, word):
    """Put each word in text file into adjectives table"""
    adj = Adjectives(word_type= word_type,
                        word = word)
    db.session.add(adj)
    db.session.commit()
    
    return adj

def get_words():
    """This gets all the words"""
    return Adjectives.query.all()

    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
