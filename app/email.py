from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(artist):
    token = artist.get_reset_password_token()
    send_email('[Porchfest] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[artist.email],
               text_body=render_template('email/reset_password.txt',
                                         user=artist, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=artist, token=token))
