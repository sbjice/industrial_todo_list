from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object('config.DevConfig')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# Setup Flask-login
# login_manager = LoginManager(app)
# login_manager.session_protection = "strong"

from app.mod_test.controllers import mod as test_module

# Register blueprints
app.register_blueprint(test_module)
