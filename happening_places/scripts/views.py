import os

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_sqlalchemy import SQLAlchemy

from forms import AddLocationForm
from forms import LoginForm
from forms import SignUpForm
from models import Hotspot
from models import User
from happening_places import app
from happening_places import db
from happening_places import login_manager
from happening_places.utils import sorter



@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


@app.route('/')
@app.route('/index')
def index():
    listings = Hotspot.query.all()
    return render_template('index.html', new_listings=listings)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        user = User(
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        print 'New User Added.'
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    user_listings = Hotspot.get_user_listings(current_user.id)
    return render_template('dashboard.html', listings=user_listings)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


@app.route('/listings')
def listings():
    return render_template('listings.html')


@app.route('/categories')
def categories():
    return render_template('categories.html')


@app.route('/directories')
def directories():
    return render_template('directories.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddLocationForm()
    if form.validate_on_submit():
        hotspot = Hotspot(
            name = form.name.data,
            address = form.address.data,
            description = form.description.data,
            user = current_user
        )
        db.session.add(hotspot)
        db.session.commit()
        print "saved.."
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def route_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
