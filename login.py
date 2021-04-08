"""Log in processing using Flask_login and WTForms"""
from model import User
from crud import login_check

#Reference to:https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    """Login form with validation from wtforms"""
    username = StringField('username', validators=[InputRequired(message="Enter your Username")])
    #import login_check from crud.py 
    password = PasswordField('password', validators=[InputRequired(message="Enter your password")])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Register form with the required elements!"""
    username = StringField('username', validators=[InputRequired(message="Enter a desired Username"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Enter a desired Password"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pwd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passsword needs to match")])

    def check_by_username(self, username):
        """Check if username is taken"""
        user_ = User.query.filter_by(username=username.data).first()
        if user_:
            raise ValidationError("Username taken, please choose another one")
    submit = SubmitField("Register")