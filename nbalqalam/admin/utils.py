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