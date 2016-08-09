from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from happening_places import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(200), nullable=False, unique=True)
    username = db.Column(db.String(500), nullable=False, unique=True)
    status = db.Column(db.String(50), default='unverified')
    role = db.Column(db.String(50), default='user')
    hotspots = db.relationship('Hotspot', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User: '{}'>".format(self.username)

    @property
    def password(self):
        raise AttributeError('password: Write Only Field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
