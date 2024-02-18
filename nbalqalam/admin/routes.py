from flask import Blueprint, render_template, abort, flash, request, url_for, redirect, jsonify
from nbalqalam import bcrypt, db
from flask_login import current_user, login_required
from nbalqalam.main.models import Post
from nbalqalam.user.models import User
from nbalqalam.user.utils import save_profile_picture
from nbalqalam.admin.forms import CreateUserForm, BroadcastMessage
from .utils import send_mail
import json
admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@login_required
def dashboard():
    number_of_posts = len(Post.query.all())
    number_of_users = len(User.query.all())
    if current_user.is_admin:
        pass
    else:
        abort(403)
    return render_template('admin/dashboard.html', number_of_posts = number_of_posts, number_of_users = number_of_users, title='Dashboard')

@admin.route('list-users/')
@login_required
def list_users():
    if current_user.is_admin:
        users = User.query.all()[::-1]
    else:
        abort(403)
    return render_template('admin/list-users.html', users = users, title='All Users')

@admin.route('broadcast/')
@login_required
def broadcast_message():
    form = BroadcastMessage()
    
    if current_user.is_admin:
        users = User.query.all()[::-1]
    else:
        abort(403)
    return render_template('admin/broadcast-message.html', users=users, form=form, title='Broadcast Message')

@admin.route('create-user/', methods=['POST', 'GET'])
@login_required
def create_user():
    form = CreateUserForm()
    if current_user.is_admin:
        if request.method == 'POST':
            if form.validate_on_submit():
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(
                    firstname = form.firstname.data,
                    lastname = form.lastname.data,
                    email = form.email.data,
                    password = password,
                    contact_info = form.contact_info.data,
                    address = form.address.data,
                    is_student = form.student.data,
                    is_admin = form.admin.data,
                    is_student_admin = form.student_admin.data,
                    email_verified = True
                )
                if form.profile_picture.data:
                    filename = save_profile_picture(form.profile_picture.data)
                    user.photo = filename

                db.session.add(user)
                db.session.commit()
                flash('New User Created Successfully', 'success')
                return redirect(url_for('admin.list_users'))
    else:
        abort(403)
    return render_template('admin/create-user.html', form=form, title='Create User')

@admin.route('posts/', methods=['POST', 'GET'])
@login_required
def list_posts():
    all_posts = Post.query.all()
    
    if current_user.is_admin:
        pass
    else:
        abort(403)
    return render_template('admin/post-list.html', all_posts = all_posts, title='Posts')

@admin.route('send-broadcast-message/', methods=['POST', 'GET'])
def send_broadcast_messages():
    message = request.form['message']
    subject = request.form['subject']
    users = request.form['users']
    users = json.loads(users)['list_users']
    if len(users) < 1:
        return jsonify({'error': 'No Users Selected'})
    else:
        for user in users:
            name = user['name']
            email = user['email']
            send_mail(email, subject, message)
        return jsonify({'success': 'Messages sent successfully'})