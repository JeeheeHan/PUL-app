"""Create, read, update and delete"""

from model import *

def create_user(eml, pwd):
    """Create and return a new user."""

    user = User(email=eml, password=pwd)

    db.session.add(user)
    db.session.commit()

    return user

def login_check(email, password):
    """Check if email matches password"""
    try: 
        user = User.query.filter(User.email == email).first()
        password_by_email = user.password

        if password == password_by_email:
            return user.user_id
    except:
        pass


