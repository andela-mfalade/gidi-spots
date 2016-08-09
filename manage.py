import os

from happening_places import db
from happening_places import create_app

from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand

workenv = os.getenv('HOTSPOT_ENV') or 'dev'
app = create_app(workenv)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
