import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure DB
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisIsTheKeyToTheKingdomHowdy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hotspots.db')
db = SQLAlchemy(app)


# Configure Auth
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

# Configure Moment
moment = Moment(app)

from scripts import forms
from scripts import models
from scripts import views
from utils import sorter
