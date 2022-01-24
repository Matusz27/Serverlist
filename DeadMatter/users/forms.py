from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from DeadMatter.models import User
from DeadMatter import bcrypt




class Reg_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)], render_kw={"placeholder": "Password"})

    password_Com = PasswordField('Password_Com', validators=[EqualTo(
        'password')], render_kw={"placeholder": "Password Confirmation"})

    submit = SubmitField("Sign up")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is already in use!')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError('Username is already in use!')


class Login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={
                        "placeholder": "Email"})

    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             "placeholder": "Password"})

    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data.lower()).first()
        if not email:
            raise ValidationError('No account found with this email')


class Acount_update_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        "placeholder": "Email"})

    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is already in use!')

    def validate_username(self, username):
        if username.data != current_user.username:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValidationError('Username is already taken')


class request_reset(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        "placeholder": "Email"})

    submit = SubmitField("Request reset")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError("Email wasn't found!")


class reset_password(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=4)], render_kw={"placeholder": "Password"})

    password_Com = PasswordField('Password_Com', validators=[EqualTo(
        'password')], render_kw={"placeholder": "Password Confirmation"})

    submit = SubmitField("Reset password")
