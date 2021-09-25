from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required,Email
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Introduce yourself to the world', validators = [Required()])
    submit = SubmitField('submit')
class BlogForm(FlaskForm):
    title = TextAreaField('Your Blog Title', validators=[Required()])
    content = TextAreaField('Your Blog Content', validators=[Required()])
    submit = SubmitField('Submit')
class CommentForm(FlaskForm):
      content = TextAreaField('Please leave a comment',validators=[Required()])
      submit = SubmitField('Comment')
class BlogUpdate(FlaskForm):
      title = StringField('Title',validators = [Required()])
      content = TextAreaField('Content',validators = [Required()]) 
      submit = SubmitField('submit') 
