from flask import Blueprint, render_template, url_for, redirect
from DeadMatter.models import Servers

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    server = Servers.query.all()
    return render_template('index.html', servers=server)

