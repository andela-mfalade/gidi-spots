from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from . import listing
from .. import db
from .forms import AddLocationForm
from happening_places.models import Hotspot


@listing.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('add.html', form=form)


@listing.route('/all')
def listings():
    return render_template('listings.html')
