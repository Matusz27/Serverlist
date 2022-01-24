from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from DeadMatter import db, bcrypt, mail
from DeadMatter.users.forms import (Reg_form, Login_form, Acount_update_form,
                              request_reset, reset_password)
from DeadMatter.models import User, Ranks
from DeadMatter.users.utils import picture_save, send_reset_email, send_validation_email

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f"Welcome {user.username}", 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
            else:
                form.password.errors = {"Invalid password"}
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Reg_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data.lower(), password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(
                f"Your account has been created! You now can login, comfirmation email has been send", 'success')
            send_validation_email(user)
            return redirect(url_for('users.login'))
        except:
            flash(f"There was an error!", 'danger')
    return render_template('register.html', form=form)


@users.route('/logout', methods=['GET'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/settings', methods=['GET'])
@login_required
def settings():
    image_file = url_for(
        'static', filename="img/Profile_pics/" + current_user.image_file)
    return render_template('settings.html', image_file=image_file)


@users.route('/account/<string:username>', methods=['GET'])
def account(username):
    user = User.query.filter_by(username=username).first()
    if user:
        image_file = url_for(
            'static', filename="img/Profile_pics/" + user.image_file)
        return render_template('account.html', image_file=image_file, user=user)
    else:
        abort(404)


@users.route('/passwordreset', methods=['GET', 'Post'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = request_reset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f"The email has been send, should be in your inbox soon", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset.html', form=form)


@users.route('/passwordreset/<token>', methods=['GET', 'Post'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if not user:
        flash(f"The link is expired or invalid!", 'warning')
        return redirect(url_for('reset_request'))
    form = reset_password()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        try:
            user.password = hashed_password
            db.session.commit()
            flash(f"Your password has been changed!", 'success')
            return redirect(url_for('users.login'))
        except:
            flash(f"There was an error!", 'danger')
    return render_template('reset_form.html', form=form)


@users.route('/validate')
@login_required
def validation_request():
    user = User.query.filter_by(username=current_user.username).first()
    send_validation_email(user)
    flash(f"The email has been send, should be in your inbox soon", 'info')
    return redirect(url_for('users.login'))


@users.route('/validate/<token>')
def validation(token):
    user = User.verify_reset_token(token)
    if not user:
        flash(f"The link is expired or invalid!", 'warning')
        return redirect(url_for('main.index'))
    if user.email_conf:
        flash(f"Your email is aready validated!", 'success')
        return redirect(url_for('main.index'))
    try:
        user.email_conf = True
        db.session.commit()
        flash(f"Your email has been validated!", 'success')
    except:
        flash(f"There was an error!", 'danger')
    return redirect(url_for('main.index'))
