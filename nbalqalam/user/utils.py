import os
import secrets
from nbalqalam import app, mail
from flask_mail import Message

def send_mail(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
        )
    mail.send(msg)

def save_profile_picture(image, location=os.path.join(app.root_path, 'static/images/profile-pictures')):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(image.filename)
    new_filename = f'{random_hex}{ext}'
    picture_path = os.path.join(location, new_filename)
    image.save(picture_path)
    return new_filename