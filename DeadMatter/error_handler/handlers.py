from flask import Blueprint, render_template

error_handler = Blueprint('error_handler', __name__)


@error_handler.app_errorhandler(404)
def E404(error):
    return render_template('errors/404.html'), 404


@error_handler.app_errorhandler(403)
def E403(error):
    return render_template('errors/403.html'), 403


@error_handler.app_errorhandler(500)
def E500(error):
    return render_template('errors/500.html'), 500
