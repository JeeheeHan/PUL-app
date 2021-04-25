"""Log in processing using Flask_login and WTForms"""
from model import User
from crud import login_check

#Reference to:https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    """Login form with validation from wtforms"""
    username = StringField('username', validators=[InputRequired(message="Enter your Username")])
    #import login_check from crud.py 
    password = PasswordField('password', validators=[InputRequired(message="Enter your password")])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Register form with the required elements!"""
    username = StringField('username', validators=[InputRequired(message="Enter your Username"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Enter your Password"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pwd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passsword needs to match")])
    submit = SubmitField("Register")
    def validate_username(self, username):
        #WTF forms will automatically invoke these
        """Check if username is taken"""
        user_ = User.query.filter_by(username=username.data).first()
        if user_ is not None:
            raise ValidationError("Username taken, please choose another one")

class UserprofileForm(FlaskForm):
    """Edit form to change username or password"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    new_password = PasswordField('new password', validators=[InputRequired(message="Enter a new desired Password"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_new_pswd = PasswordField('confirm_new_pwd', validators=[InputRequired(message="Confirm new password"), EqualTo('new_password', message="Passsword needs to match")])
    submit = SubmitField("Update")

class WordsForm(FlaskForm):
    """Form to get polarity of requested text"""
    analysis = SelectField(u'Opinion Mining', choices=[('pat', 'Pattern Library'), ('naive', 'NaiveBayers from Movie reviews')])
    text = TextAreaField(u'Text', validators=[Length(max=200)])
