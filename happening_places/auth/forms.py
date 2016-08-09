from flask_wtf import Form
from wtforms.fields import BooleanField
from wtforms.fields import PasswordField
from wtforms.fields import StringField
from wtforms.fields import SubmitField
from flask.ext.wtf.html5 import URLField, EmailField
from wtforms.validators import InputRequired, url, Email
from wtforms.validators import Regexp, Length, ValidationError

from happening_places.models import User


class SignUpForm(Form):
    email = EmailField('email', validators=[InputRequired(), Email()])
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    username = StringField('username', validators=[
        InputRequired(),
        Length(3,50),
        Regexp('^[A-Za-z0-9_{3,}$]', message="Username must consist of only letters, numbers and underscores")
    ])
    password = PasswordField('password', validators=[InputRequired()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken')


class LoginForm(Form):
    username= StringField('Your Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me Logged In')
