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
  