from datetime import datetime

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
