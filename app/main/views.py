from . import main
from flask import render_template, request, redirect, url_for, abort,flash
from ..models import User, Blog, Comment, Sub
from flask_login import login_required, current_user
from .forms import BlogForm, UpdateProfile, BlogUpdate, CommentForm
from .. import db, photos

@main.route('/')
def index():
  posts = Blog.query.all()
  blogs = posts.reverse()
  # status = None
  # if current_user.posts:
  #   status = 'Author'
  # else:
  #   status = 'Dedicated Reader'
  return render_template('index.html', blogs=blogs)  
@main.route('/create_new',methods = ['GET','POST'])
@login_required  
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
       title = form.title.data
       content = form.content.data
       user_id = current_user._get_current_object().id
       new_blog_obj = Blog(content = content,title =title,user_id=user_id)
       new_blog_obj.save_blog()
       return redirect(url_for('main.index'))
    return render_template('new_blog.html', form = form)

@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
@login_required
def comment(blog_id):
    form = CommentForm()
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    blog = Blog.query.get(blog_id)
    if form.validate_on_submit():
        content = form.content.data
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(blog_id=blog_id,content=content, user_id=user_id)
        new_comment.save_comment()   
        return redirect(url_for('.comment', blog_id=blog_id))
    print(blog)
    return render_template('comment.html', form = form, blog = blog, all_comments=all_comments)    


@main.route('/index/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete(id):
    current_post = Blog.query.filter_by(id=id).first()
    if current_post.user != current_user:
       abort(404)
    db.session.delete(current_post)   

@main.route('/index/<int:id>/delcomm',methods = ['GET','POST'])
@login_required
def delete_comm(id):
    current_comm = Comment.query.filter_by(id=id).first()
    if current_comm.user != current_user:
       abort(404)
    db.session.delete(current_comm)  

