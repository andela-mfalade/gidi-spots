from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from .import auth
from .. import db
from .forms import LoginForm
from .forms import SignUpForm
from happening_places.models import User
from happening_places.models import Hotspot


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/dashboard')
@login_required
def dashboard():
    user_listings = Hotspot.get_user_listings(current_user.id)
    return render_template('dashboard.html', listings=user_listings)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
