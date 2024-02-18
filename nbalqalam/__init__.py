from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'jhdgfiw8745y4378d74736db4s'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECURITY_PASSWORD_SALT'] = 'dsftgytfycdgyfgewfwe76'
app.config.update(dict(
    DEBUG= True,
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'abuakar21@gmail.com',
    MAIL_PASSWORD = 'wxje jdiq ubhn zdux',
    MAIL_DEFAULT_SENDER = 'NB@alqalam'
))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail=Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
from nbalqalam.user.routes import user
from .main.routes import main
from .admin.routes import admin
#Blueprints
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(main, url_prefix='/')


#mail settings


#gmail authentication


#mail accounts
