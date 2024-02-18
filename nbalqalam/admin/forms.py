from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.html5 import EmailField
from nbalqalam.user.models import User

class CreateUserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=3, max=100)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    contact_info = StringField('Phone Number')
    profile_picture = FileField('Upload Profile Picture', [FileAllowed(('jpg', 'png'))])
    address = TextAreaField('Address')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    student = BooleanField('Student User')
    student_admin = BooleanField('Student-Admin User')
    admin = BooleanField('Admin User')
    submit = SubmitField('Create User')
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('User with this email already exists')

class BroadcastMessage(FlaskForm):
    subject = StringField('Subject')
    body = TextAreaField('Subject', validators=[DataRequired()])
    submit = SubmitField('Send Message')