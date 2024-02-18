import os
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import current_user
from .forms import CreatePost, EditPost, CreateClassNotification
from.models import Post, ClassNotification
from nbalqalam import db
from .utils import save_post_image
from flask_login import login_required, current_user
from nbalqalam.user.models import User, app
main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    return render_template('main/index.html')

@main.route('home/')
@login_required
def homepage():
    posts = Post.query.all()[::-1]
    try:
        headlines = Post.query.all()[:5][::-1]
    except:
        headlines = Post.query.all()[:][::-1]
    return render_template('main/homepage.html', headlines = headlines, posts=posts)

@main.route('create-post/', methods=['POST', 'GET'])
@login_required
def create_post():
    if current_user.is_admin or current_user.is_student_admin:
        form = CreatePost()
        if request.method == 'POST':
            
            if form.validate_on_submit():
                slug = form.slug.data
                if not form.slug.data:
                    try:
                        slug = '-'.join(form.title.data[:15].split(' '))
                    except IndexError:
                        slug = '-'.join(form.title.data[:].split(' '))
                post = Post(
                    title = form.title.data,
                    slug = slug,
                    body = form.body.data,
                    author_id = current_user.id
                )
                if form.post_image.data:
                    filename = save_post_image(form.post_image.data)
                    post.post_image = filename
                db.session.add(post)
                db.session.commit()
                post = Post.query.filter_by(title=form.title.data, body=form.body.data).first()
                flash('Post created successfully', 'success')
                return redirect(url_for('main.post_details', id=post.id, slug=post.slug))
    else:
        abort(403)
    return render_template('main/create-post.html', form=form, title='Create Post')

@main.route('posts/<id>/<slug>')
@login_required
def post_details(id, slug):
    try:
        recent_posts = Post.query.all()[:10][::-1]
    except:
        recent_posts = Post.query.all()[:][::-1]
    post = Post.query.get_or_404(id)
    post_image_url = url_for('static', filename=os.path.join('images', 'post-images', f'{post.post_image}'))
    post_image_url=os.path.join(url_for('static', filename='images'), 'post-images', f'{post.post_image}')
    author = User.query.get(post.author_id)
    return render_template('main/post-details.html', post=post, post_image_url=post_image_url, recent_posts=recent_posts, author=author, title=post.title[:])

@main.route('posts/<id>/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(id, slug):
    post = Post.query.get_or_404(id)
    if post.author_id == current_user.id or current_user.is_admin:
        form = EditPost()
        if request.method == 'GET':
            form.title.data = post.title
            form.slug.data = post.slug
            form.body.data = post.body
        elif request.method == 'POST':
            post.title = form.title.data
            post.body = form.body.data

            post.slug = form.slug.data
            if not form.slug.data:
                try:
                    post.slug = '-'.join(form.title.data[:15].split(' '))
                except IndexError:
                    post.slug = '-'.join(form.title.data[:].split(' '))
            if form.post_image.data:
                    filename = save_post_image(form.post_image.data)
                    if post.post_image != 'default.jpg':
                        try:
                            os.remove(os.path.join(app.root_path, 'static/images/post-images', f'{post.post_image}'))
                        except FileNotFoundError:
                            pass
                    post.post_image = filename
            db.session.commit()
            flash('Post was edited successfully', 'success')
            return redirect(url_for('main.post_details', id=post.id, slug = post.slug))
    else:
        abort(403)
    return render_template('main/edit-post.html', form=form, title='Edit Post')

@main.route('posts/<id>/<slug>/delete')
@login_required
def delete_post(id, slug):
    post = Post.query.get_or_404(id)
    if current_user.is_admin or (current_user.id == post.author_id):
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
        if current_user.is_admin:
            return redirect(url_for('admin.list_posts'))
        else:
            return redirect(url_for('main.homepage'))
    else:
        abort(403)

@main.route('class/')
@login_required
def class_view():
    form=CreateClassNotification()
    if (current_user.is_admin or current_user.is_student) or current_user.is_student_admin:
        class_notifications = ClassNotification.query.all()[::-1]
    else:
        abort(403)
    return render_template('main/class-view.html', form = form, class_notifications = class_notifications)

@main.route('class/', methods=['POST', 'GET'])
@login_required
def post_class_notification():
    form = CreateClassNotification()
    if current_user.is_admin or current_user.is_student_admin:
        if request.method == 'POST':
            if form.validate_on_submit():
                post = ClassNotification(
                    title = form.title.data,
                    body = form.body.data
                )
                if form.post_image.data:
                    filename = save_post_image(form.post_image.data)
                    post.post_image = filename
                db.session.add(post)
                db.session.commit()
                flash('Post Created Successfully', 'success')
            return redirect(url_for('main.class_view'))
    else:
        abort(403)

@main.route('class-notification/<id>/delete', methods=['GET'])
@login_required
def delete_class_notification(id):
    if current_user.is_admin or current_user.is_student_admin:
        notification = ClassNotification.query.get_or_404(id)
        db.session.delete(notification)
        db.session.commit()
        flash('Post deleted successfully', 'success')
        return redirect(url_for('main.class_view'))
    else:
        abort(403)