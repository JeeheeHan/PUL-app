"""Log in processing using Flask_login and WTForms"""
from model import User
from crud import login_check

#Reference to:https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    """Login form with validation from wtforms"""
    username = StringField(u'username', validators=[InputRequired(message="Enter your Username")], render_kw={"placeholder": "Your Username", "class":"login"})
    password = PasswordField(u'password', validators=[InputRequired(message="Enter your password")],render_kw={"placeholder": "Your Password","type":"password","class":"login"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Register form with the required elements!"""
    username = StringField(u'username', validators=[InputRequired(message="Enter your Username"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")], render_kw={"placeholder": "Username","class":"login"})
    password = PasswordField(u'password', validators=[InputRequired(message="Enter your Password"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")],render_kw={"placeholder": "Password","type":"password","class":"login"})
    confirm_pswd = PasswordField(u'confirm_pwd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passsword needs to match")], render_kw={"placeholder": "Confirm Password","type":"password","class":"login"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        #WTF forms will automatically invoke these
        """Check if username is taken"""
        user_ = User.query.filter_by(username=username.data).first()
        if user_ is not None:
            raise ValidationError("Username taken, please choose another one")

class UserprofileForm(FlaskForm):
    """Edit form to change username or password"""
    username = StringField(u'username', validators=[DataRequired()], render_kw={"type":"hidden"})
    password = PasswordField(u'password', validators=[DataRequired()],render_kw={"placeholder": "Current Password","type":"password","class":"login"} )
    new_password = PasswordField(u'new password', validators=[InputRequired(message="Enter a new desired Password"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")], render_kw={"placeholder": "New Password","type":"password","class":"login"})
    confirm_new_pswd = PasswordField(u'confirm_new_pwd', validators=[InputRequired(message="Confirm new password"), EqualTo('new_password', message="Passsword needs to match")],render_kw={"placeholder": "Confirm New Password","type":"password","class":"login"})
    submit = SubmitField("Update")

class WordsForm(FlaskForm):
    """Form to get polarity of requested text"""
    analysis = SelectField(u'Opinion Mining', choices=[('pat', 'Dictionary based (Pattern Library)'), ('naive', 'Movie Ratings based(NaiveBayers)')], render_kw={"class":"wordform"})
    text = TextAreaField(u'Text', validators=[Length(max=200)],render_kw={"placeholder":"Polarity ranges from most positve being 1 while at worst -1 for negativity", "class":"wordform"})
    submit = SubmitField("Run")