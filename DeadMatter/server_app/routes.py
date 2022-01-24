from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from flask_login import current_user, login_required
from DeadMatter import db
from DeadMatter.server_app.forms import (Server_submit, Server_update)
from DeadMatter.models import Ranks, Servers, Country
from DeadMatter.server_app.utils import picture_save


server_app = Blueprint('server_app', __name__)


@server_app.route('/server/new', methods=['GET', "POST"])
@login_required
def new_server():
    form = Server_submit()
    if len(current_user.servers_id) >= 2:
        flash(f"You have reached the server limit!", 'warning')
        return redirect(url_for('main.index'))
    if not current_user.email_conf:
        flash(f"You have to validate your email first!", 'warning')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        picture_file = None
        if form.picture.data:
            picture_file = picture_save(form.picture.data)

        server = Servers(name=form.name.data, server_IP=form.server_IP.data,
                         port=form.port.data,description=form.description.data,
                         discord=form.discord.data, website=form.website.data, 
                         image_file=picture_file, country_id=form.country.data, 
                         author=current_user)
        try:
            db.session.add(server)
            db.session.commit()
            flash(f"Your Server has been added to our list!", 'success')
            return redirect(url_for('main.index'))
        except:
            flash(f"There was an error when adding your server!", 'danger')

    return render_template('submit.html', form=form)


@server_app.route('/server/<int:server_id>', methods=['GET', "POST"])
def server_page(server_id):
    server = Servers.query.get_or_404(server_id)
    return render_template('server.html', server=server)


@server_app.route('/server/<int:server_id>/update', methods=['GET', "POST"])
@login_required
def server_update(server_id):
    server = Servers.query.get_or_404(server_id)
    form = Server_update(country=server.country.id)
    if server.author != current_user and current_user.rank_id != 2:
        abort(403)
    if form.validate_on_submit():
        picture_file = "default.png"
        if server.image_file != picture_file:
            picture_file = server.image_file
        if form.picture.data:
            picture_file = picture_save(form.picture.data)
        server.name = form.name.data
        server.server_IP = form.server_IP.data
        server.port = form.port.data
        server.description = form.description.data
        server.discord = form.discord.data
        server.website = form.website.data
        server.country_id = form.country.data
        server.image_file = picture_file
        try:
            db.session.commit()
            flash(f"Your Server has been edited!", 'success')
            return redirect(url_for('main.index'))
        except:
            flash(f"There was an error while editing your server!", 'danger')
    if request.method == 'GET':
        form.name.data = server.name
        form.server_IP.data = server.server_IP
        form.port.data = server.port
        form.description.data = server.description
        form.discord.data = server.discord
        form.website.data = server.website
    return render_template('server_update.html', form=form)


@server_app.route('/server/<int:server_id>/delete', methods=["POST"])
@login_required
def delete_post(server_id):
    server = Servers.query.get_or_404(server_id)
    if server.author != current_user and current_user.rank_id != 2:
        abort(403)
    try:
        db.session.delete(server)
        db.session.commit()
        flash(f"Your Server has been deleted!", 'success')
        return redirect(url_for('main.index'))
    except:
        flash(f"There was an error while deleting your server!", 'danger')
