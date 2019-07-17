from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from teston import app
#app.config.from_object('app.config')

# configuration
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.168.169/logins'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from apps.Auth.model1 import  db
db.init_app(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
