from nbalqalam import db
from datetime import datetime
from nbalqalam.user.models import User
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    post_image = db.Column(db.String(255), nullable=False, default='default.png')

class ClassNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    post_image = db.Column(db.String(255), nullable=False, default='default.png')