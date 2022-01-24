import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import url_for
from flask_login import current_user
from DeadMatter import mail, app


def send_page_report_email(form):
    if current_user.is_authenticated:
        user = current_user.username
    else:
        user = "Annon"
    usermail = form.email.data
    msg = Message(f'Server {form.problem.data}',
                  sender='deadmattersl@gmail.com',
                  recipients=['deadmattersl@gmail.com'])
    msg.body = f"""{usermail} {user} has send a report!
    
{form.description.data}"""
    mail.send(msg)


def send_server_report_email(form):
    if current_user.is_authenticated:
        user = current_user.username
    else:
        user = "Annon"
    usermail = form.email.data
    msg = Message(f'Server List Item is/has {form.problem.data}',
                  sender='deadmattersl@gmail.com',
                  recipients=['deadmattersl@gmail.com'])
    msg.body = f"""{usermail} {user} has send a report!
    
{form.description.data}"""
    mail.send(msg)
