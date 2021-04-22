from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    owner = db.Column(db.Integer, nullable=False)
    # owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    deadline = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password_hash = db.Column(db.String(250), nullable=False)
    # tasks = relationship("Task", backref="owner")



