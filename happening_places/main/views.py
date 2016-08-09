from flask import render_template

from . import main
from happening_places import login_manager
from happening_places.models import Hotspot
from happening_places.models import User


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


@main.route('/')
def index():
    listings = Hotspot.query.all()
    return render_template('index.html', new_listings=listings)


@main.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


@main.route('/categories')
def categories():
    return render_template('categories.html')


@main.route('/directories')
def directories():
    return render_template('directories.html')


@main.app_errorhandler(403)
def server_error(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def route_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@main.app_context_processor
def server_error():
    return dict(all_tags=[
        'lifestyle',
        'hotels',
        'bars',
        'supermarkets',
        'movies',
        'outdoors'
    ])
