from importlib.machinery import FileFinder
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
from flask_wtf.file import FileField
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please enter a different username')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please enter a different email address')

class UploadForm(FlaskForm):
    file = FileField()
