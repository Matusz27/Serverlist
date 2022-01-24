import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import url_for
from DeadMatter import mail, app









def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='deadmattersl@gmail.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, follow the link:
{url_for('users.password_reset', token=token, _external=True)}

If you hadn't make this request, ignore this email.

    Have a good day! 
   DeadMatter server List
"""
    mail.send(msg)


def send_validation_email(user):
    token = user.get_reset_token()
    msg = Message('Email validation',
                  sender='deadmattersl@gmail.com',
                  recipients=[user.email])
    msg.body = f"""To Validate your email, follow the link:
{url_for('users.validation', token=token, _external=True)}

If you hadn't make this request, ignore this email.

    Have a good day! 
   DeadMatter server List
"""
    mail.send(msg)


def picture_save(picture_data):
    random_name = secrets.token_hex(8)
    _, p_ext = os.path.splitext(picture_data.filename)
    picture_new_name = random_name + p_ext
    picture_path = os.path.join(
        app.root_path, 'static\img\Server_pics', picture_new_name)

    output_size = (500, 500)
    i = Image.open(picture_data)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_new_name
