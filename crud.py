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

    username = form.username.data
    #https://wtforms.readthedocs.io/en/2.3.x/fields/
    password = field.data

    try: 
        user = User.query.filter_by(username=username).first()
        password_by_username = user.password

        if password == password_by_username:
            return login_user(user)
    except:
        raise ValidationError("Wrong credentials, please try again")




if __name__ == '__main__':
    from server import app
    connect_to_db(app)
