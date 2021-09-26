from app import create_app,db
from flask_script import Manager,Server
from app.models import User, Blog, Comment, Sub
from  flask_migrate import Migrate, MigrateCommand


app = create_app('production')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=3).run(tests)
@manager.shell    
def make_shell_context():
    return dict(app = app,db = db,User = User, Blog = Blog,Comment = Comment, Sub = Sub)        

if __name__ == '__main__':
    manager.run()    