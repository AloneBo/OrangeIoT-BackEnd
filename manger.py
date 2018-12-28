from iotweb import create_app, db, models
from flask_script import Manager
import flask_migrate


app = create_app(config_name='dev')

manger = Manager(app)

flask_migrate.Migrate(app, db)

manger.add_command("db", flask_migrate.MigrateCommand)

if __name__ == '__main__':
    manger.run()


