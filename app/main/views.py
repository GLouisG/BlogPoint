from . import main
from flask import render_template, request, redirect, url_for, abort,flash
from ..models import User, Blog, Comment, Sub
from flask_login import login_required, current_user
from .forms import UpdateProfile, PitchForm, CommentForm
from .. import db, photos

@main.route('/')
def index():
  blogs = Blog.query.all()
  posts = blogs.reverse()
  # status = None
  # if current_user.posts:
  #   status = 'Author'
  # else:
  #   status = 'Dedicated Reader'
  return render_template('index.html', posts=posts)  