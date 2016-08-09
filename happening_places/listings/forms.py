from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired

from happening_places.models import Hotspot


class AddLocationForm(Form):
    name = StringField('name_of_hotspot', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])
    description = StringField('description', validators=[InputRequired()])
