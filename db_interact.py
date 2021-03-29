from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    owner = db.Column(db.String(250), nullable=False)
    deadline = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, nullable=False)


