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
  sub = db.relationship('Sub', backref='user', lazy = True)
  @property
  def password(self):
      raise AttributeError("You can't read the password attribute" )
  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)
  def verify_password(self, password):
    return check_password_hash(self.pass_secure, password)
  def __repr__(self):
      return f'User:{self.username}'    

class Blog (db.Model):
  __tablename__ = 'blogs'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  content = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  post_time = db.Column(db.DateTime, default=datetime.utcnow())
  comments = db.relationship('Comment', backref='blog', lazy = True)

  def save_blog(self):
      db.session.add(self)
      db.session.commit()
  def delete_blog(self):
      db.session.delete(self)
      db.session.commit()  

  @classmethod
  def get_blogs(cls):
      blog = Blog.query.filter_by(id = id).all()
      return blog

  def __repr__(self):
        return f'Blog:{self.content}'

class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
  content = db.Column(db.String(), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()
  @classmethod
  def get_comments(cls, blog_id):
    comments = Comment.query.filter_by(blog_id=blog_id)
    return comments
  @classmethod
  def delete_comment(cls, id):
        unwanted = Comment.query.filter_by(id = id).first()
        db.session.delete(unwanted)
        db.session.commit() 
  @classmethod
  def clear_comment(cls):
        Comment.all_comments.clear()       

  def __repr__(self):
    return f'Comment:{self.content}'   

class Sub(db.Model):   
  __tablename__ = 'subs'
  id = db.Column(db.Integer, primary_key=True)  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  email_add = db.Column(db.String())
  def save_sub(self):
      db.session.add(self)
      db.session.commit()

  def __repr__(self):
        return f'Sub:{self.email_add}'

class Quotes:
      def __init__(self,id, author,quote):
            self.id =id
            self.author = author
            self.quote = quote    