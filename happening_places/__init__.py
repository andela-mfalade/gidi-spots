import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
# from flask_debugtoolbar import DebugToolbarExtension

from .config import config_by_name


# Initialize And Configure App Extensions
db = SQLAlchemy()
moment = Moment()
# toolbar = DebugToolbarExtension()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Install App Extensions
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    # toolbar.init_app(app)

    from .auth import auth as auth_blueprint
    from .listings import listing as listing_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(listing_blueprint, url_prefix='/listings')

    return app
