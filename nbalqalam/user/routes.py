import os
from nbalqalam import app
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from .forms import LoginForm , SignupForm, RequestPasswordReset, ResetPassword, EditProfileForm
from nbalqalam import bcrypt, db
from .models import User
from.utils import send_mail, save_profile_picture
from flask_login import login_user, current_user, logout_user, login_required
user = Blueprint('user', __name__, template_folder='templates')

@user.route('login/', methods=['POST', 'GET'])

def login():
    form = LoginForm()
    if not current_user.is_authenticated:
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                    next_page = request.args.get('next')
                    login_user(user, remember=form.remember_me.data)                    
                    return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
                else:
                    flash('Email or Password is incorrect', 'danger')
    else:
        return redirect(url_for('main.homepage'))
    return render_template('user/login.html', form=form, title='Login')

@user.route('logout/', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@user.route('signup/', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if not current_user.is_authenticated:
        if request.method == 'POST':
            if form.validate_on_submit():
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(
                    firstname = form.firstname.data,
                    lastname = form.lastname.data,
                    email = form.email.data,
                    password = password,
                    is_student = form.student.data
                )
                user.email_verified = True
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('user.login'))
    else:
        return redirect(url_for('main.homepage'))
    return render_template('user/signup.html', form=form, title='Sign Up')

@user.route('request-password/', methods=['POST', 'GET'])
def request_password_reset():
    form = RequestPasswordReset()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user:
                token = user.generate_confirmation_token()
                reset_password_url = url_for('user.reset_password', token=token, _external=True)
                html = render_template('user/mail/reset-password.html', reset_password_url = reset_password_url)
                subject = 'Reset Password'
                send_mail(user.email, subject, html)
                flash('A password reset link has been sent to your email address. Please check your email.', 'success')
                return redirect(url_for('user.login'))
    return render_template('user/request-password-reset.html', form=form, title='Request Password Reset')

@user.route('reset-password/<token>/', methods=['POST', 'GET'])
def reset_password(token):
    form = ResetPassword()
    if request.method == 'POST':
        email = User.confirm_token(User, token=token)
        if not email:
            flash('Password reset link is invalid or has expired', 'danger')
        else:
            user = User.query.filter_by(email=email).first()
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = password
            db.session.add(user)
            db.session.commit()
            flash('Password reset successfully. Please Login.', 'success')
            return redirect(url_for('user.login'))
    return render_template('user/reset-password.html', token=token, form=form, title='Reset Password')

@user.route('profile/<user_id>/')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(int(user_id))
    return render_template('user/view-profile.html', user = user, title='Profile')

@user.route('profile/<user_id>/edit/', methods=['POST', 'GET'])
@login_required
def edit_profile(user_id):
    form = EditProfileForm()
    user = User.query.get_or_404(int(user_id))
    if current_user.id == user.id or current_user.is_admin:
        if request.method == 'GET':
            form.firstname.data = user.firstname
            form.lastname.data = user.lastname
            form.email.data = user.email
            form.contact_info.data = user.contact_info
            form.address.data = user.address
            form.matric_number.data = user.matric_number
            form.is_admin.data = user.is_admin
            form.is_student_admin.data = user.is_student_admin
            form.is_student.data = user.is_student
        else:
            if form.validate_on_submit():
                user.firstname = form.firstname.data
                user.lastname = form.lastname.data
                user.email = form.email.data
                user.contact_info = form.contact_info.data
                user.address = form.address.data
                user.matric_number = form.matric_number.data
                if current_user.is_admin:
                    user.is_admin = form.is_admin.data
                    user.is_student_admin = form.is_student_admin.data
                    user.is_student = form.is_student.data
                
                if form.profile_picture.data:
                    filename = save_profile_picture(form.profile_picture.data)

                    if user.photo != 'default.jpg':
                        try:
                            os.remove(os.path.join(app.root_path, 'static/images/profile-pictures', f'{user.photo}'))
                        except FileNotFoundError:
                            pass

                    user.photo = filename
                db.session.commit()
                flash('Profile Updated Successfully', 'success')
                return redirect(url_for('user.view_profile', user_id=user.id))
    else:
        abort(403)
    return render_template('user/edit-profile.html', form = form, user = user, title = 'Edit Profile')

@user.route('user/<user_id>/delete/', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    if current_user.is_admin:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User Deleted Successfully', 'success')
        return redirect(url_for('admin.list_users'))
    else:
        abort(403)