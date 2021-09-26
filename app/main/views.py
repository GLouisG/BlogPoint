from app.requests import find_quotes
from . import main
from flask import render_template, request, redirect, url_for, abort,flash
from ..models import User, Blog, Comment, Sub
from flask_login import login_required, current_user
from .forms import BlogForm, UpdateProfile, BlogUpdate, CommentForm
from .. import db, photos
from ..email import mail_message

@main.route('/')
def index():
  posts = Blog.query.all()
  blogs = posts.reverse()
  thequote = find_quotes()
  return render_template('index.html', blogs=blogs, thequote=thequote)  
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
    followers = Sub.query.filter_by(writer = current_user.username).all()   
    for subscriber in  followers:
        mail_message("New post!", "email/subscriber", subscriber.email, user=subscriber)     
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
    return redirect(url_for('.index'))

@main.route('/index/<int:id>/delcomm',methods = ['GET','POST'])
@login_required
def delete_comm(id):
    current_comm = Comment.query.filter_by(id=id).first()
    if current_comm.user != current_user:
       abort(404)
    db.session.delete(current_comm) 
    return redirect(url_for('.index')) 

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    blogs = Blog.query.filter_by(user_id = user_id).all()
    status = None
    if current_user.posts:
      status = 'Author'
    else:
      status = 'Dedicated Reader'    

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, blogs = blogs, status=status)


@main.route('/blogs/<uname>/updateprofile', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/update/<int:id>',methods = ['GET','POST'])
@login_required
def blog_updater(id):
    ablog = Blog.query.filter_by(id=id).first()
    if ablog.user != current_user:
      abort(404)
    form = BlogUpdate()
    if form.validate_on_submit():
        ablog.title = form.title.data
        ablog.content = form.content.data
        db.session.add(ablog)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_blog.html',form = form)    

@main.route('/subscription/<author>', methods = ['POST','GET'])
@login_required
def subscription(author):
    subber = Sub.query.filter_by(email=current_user.email).first()
    if subber:
       db.session.delete(subber)
       db.session.commit()
       return redirect(url_for('.index'))
    else:
      email = current_user._get_current_object().email
      writer = author  
      new_sub_object = Sub(email = email, writer=writer)
      new_sub_object.save_sub()
      return redirect(url_for('.index'))  
    return redirect(url_for('.index'))     

