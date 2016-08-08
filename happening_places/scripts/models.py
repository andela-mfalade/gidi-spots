from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from happening_places import db


categories = db.Table('hotspot_category',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('hotspot_id', db.Integer, db.ForeignKey('hotspot.id'))
)


class Hotspot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(700))
    description = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='unverified')
    _categories = db.relationship(
        'Category',
        secondary=categories,
        backref=db.backref('hotspots', lazy='dynamic')
    )

    @staticmethod
    def get_user_listings(user_id):
        return Hotspot.query.filter_by(user_id=user_id).all()

    def __repr__(self):
        return "<Hotspot '{}' '{}'>".format(self.name, self.description)


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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    def __repr__(self):
        return self.name
