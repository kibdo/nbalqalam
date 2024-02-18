from itsdangerous import URLSafeTimedSerializer
from nbalqalam import app, db
from datetime import datetime
from nbalqalam import login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable = False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    photo = db.Column(db.String(100), nullable=False, default='default.png')
    status = db.Column(db.Boolean, nullable=False, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    matric_number = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_student_admin = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=app.config['SECURITY_PASSWORD_SALT'])

    def confirm_token(cls, token, expiration=15000):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt = app.config['SECURITY_PASSWORD_SALT'],
                max_age = expiration
            )
        except:
            return False
        return email
