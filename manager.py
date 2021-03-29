from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import app, db

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='195.24.64.20', port=5000))

if __name__ == '__main__':
    manager.run()