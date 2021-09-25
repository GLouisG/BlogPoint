from sqlalchemy.orm import backref
from .import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  __tablename__='users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255),nullable=False, unique=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  bio = db.Column(db.String(255))
  pass_secure = db.Column(db.String(255))
  dp_path = db.Column(db.String())
  blog = db.relationship('Blog', backref='user', lazy =True)
  comment = db.relationship('Comment', backref='user', lazy = True)
class Blog (db.Model):
  __tablename__ = 'blogs'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  post_time = db.Column(db.DateTime, default=datetime.utcnow())
  comments = db.relationship('Comment', backref='blog', lazy = True)

  def save_blog(self):
      db.session.add(self)
      db.session.commit()

  def __repr__(self):
        return f'Blog{self.content}'