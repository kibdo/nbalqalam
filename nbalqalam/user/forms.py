from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.html5 import EmailField
from .models import User
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=3, max=100)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    student = BooleanField('I\'m a Student')
    submit = SubmitField('Sign Up')
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('User with this email already exists')
class EditProfileForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    contact_info = StringField('Phone Number')
    address = TextAreaField('Address')
    profile_picture = FileField('Change Profile Picture', [FileAllowed(('jpg', 'png'))])
    matric_number = StringField('Matric. Number')
    is_student_admin = BooleanField('Student Admin')
    is_student = BooleanField('Student')
    is_admin = BooleanField('Admin')
    submit = SubmitField('Edit')

class RequestPasswordReset(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')