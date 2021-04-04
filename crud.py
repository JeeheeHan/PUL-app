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
    
def get_user_by_email(email):
    """Return a user by email"""
    
    return User.query.filter(User.email == email).first()
    #Return the first result of this Query or None if the result doesn’t contain any row.


if __name__ == '__main__':
    from server import app
    connect_to_db(app)