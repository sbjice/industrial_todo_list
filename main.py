from flask import Flask
from flask_login import LoginManager

from db_interact import db, User
import os

from tasks.tasks import tasks_blueprint
from auth.auth import auth_blueprint


app = Flask(__name__)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db.create_all()


app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(tasks_blueprint, url_prefix='/tasks')


@app.route('/')
def home():
    return 'This is the starting page. Go to /tasks if you want to move to tasks section'


if __name__ == "__main__":
    app.run(
        debug=True,
        host='127.0.0.15',
        port=5200
    )