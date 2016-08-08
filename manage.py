from flask.ext.script import Manager
from flask.ext.script import prompt_bool
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand

from happening_places import app
from happening_places import db
from happening_places.scripts.models import Hotspot
from happening_places.scripts.models import User
from happening_places.scripts.models import Category

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    db.create_all()
    print "Initialized The Databaase."


@manager.command
def dropdb():
    if prompt_bool('Are you sure you want to lose all your data?'):
        db.drop_all()
        print "Destroyed all your data."


if __name__ == '__main__':
    manager.run()
