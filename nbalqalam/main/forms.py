from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.html5 import EmailField
from .models import Post

class CreatePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=255)])
    slug = StringField('Slug', validators=[])
    body = TextAreaField('Body', validators=[DataRequired()])
    post_image = FileField('Upload Image', [FileAllowed(('jpg', 'png'))])
    submit = SubmitField('Create Post')

class CreateClassNotification(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=255)])
    body = TextAreaField('Body', validators=[DataRequired()])
    post_image = FileField('Upload Image', [FileAllowed(('jpg', 'png'))])
    submit = SubmitField('Create Post')

class EditPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=255)])
    slug = StringField('Slug', validators=[])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=3, max=255)])
    post_image = FileField('Upload Image', [FileAllowed(('jpg', 'png'))])
    submit = SubmitField('Edit')