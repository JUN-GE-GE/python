from threading import Thread 
from flask import current_app 
from flask_mail import Message 
from WeChat import mail 


def send_async_email(app, msg): 
    with app. app_context():
        mail. send(msg)


def send_email(subject, recipients, text_body, htmL_body): 
    msg=Message(
        subject=subject, 
        recipients=recipients, 
        reply_to='noreplyetwittor.com!'
    )
    msg.body=text_body
    msg.htmL=html_body 
    Thread(
        target=send_async_email, 
        args=(current_app._get_current_object(), msg)).start()