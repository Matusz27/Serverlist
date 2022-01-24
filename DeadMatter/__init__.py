from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from DeadMatter.config import config


app = Flask(__name__)

app.config.from_object(config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from DeadMatter.users.routes import users
from DeadMatter.server_app.routes import server_app
from DeadMatter.main.routes import main
from DeadMatter.error_handler.handlers import error_handler
from DeadMatter.reports.routes import reports

app.register_blueprint(users)
app.register_blueprint(server_app)
app.register_blueprint(main)
app.register_blueprint(error_handler)
app.register_blueprint(reports)
