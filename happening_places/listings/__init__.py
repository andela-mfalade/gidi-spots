from flask import Blueprint

listing = Blueprint('listing', __name__)

from . import views
