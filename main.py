from flask import Flask, jsonify, render_template, redirect, url_for
from db_interact import db
from tasks_blueprint import tasks_blueprint
import os


app = Flask(__name__)
app.register_blueprint(tasks_blueprint, url_prefix='/tasks')
db.init_app(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        debug=True,
        host='127.0.0.15',
        port=5200
    )