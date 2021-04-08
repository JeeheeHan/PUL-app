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
            return user.user_id
    except:
        pass
        # raise ValidationError("Wrong credentials, please try again")

def save_chat_message(data):
    """Saving chat message into DB"""

    pass

def login_track(username):
    """Saving last logged into DB"""
    user = User.query.filter_by(username=username).first()
    user.last_login = datetime.utcnow()
    return user.last_login
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
