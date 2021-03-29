from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import NewTaskForm, ExistingTaskForm, RegisterForm
import datetime
import os

app = Flask(
    __name__
)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    owner = db.Column(db.String(250), nullable=False)
    deadline = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, nullable=False)


db.create_all()


def create_form_from_task(task: Task):
    form = ExistingTaskForm()
    form.owner.data = task.owner
    form.deadline.data = datetime.datetime.strptime(task.deadline, "%Y-%m-%d").date()
    form.done.data = task.done
    form.id.data = task.id
    form.text.data = task.text
    return form


def create_existing_tasks_forms():
    tasks = Task.query.all()
    task_forms = []
    for task in tasks:
        form = create_form_from_task(task)
        task_forms.append(form)
    return task_forms


@app.route('/', methods=["GET"])
def home():
    new_task_form = NewTaskForm()
    task_forms = create_existing_tasks_forms()
    return render_template('index.html', tasks=task_forms, form=new_task_form)


@app.route('/tasks')
def get_tasks():
    tasks = create_existing_tasks_forms()
    return render_template('tasks.html', tasks=tasks)


@app.route('/new_task', methods=["POST"])
def new_task():
    form = NewTaskForm()
    if form.validate_on_submit():
        task = Task(
            text=form.text.data,
            owner=form.owner.data,
            deadline=form.deadline.data if form.deadline.data else str(datetime.date.today()),
            done=form.done.data
        )
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('get_tasks'))


@app.route('/change_tasks/<int:task_id>', methods=["POST"])
def change_tasks(task_id):
    form = ExistingTaskForm()
    if form.validate_on_submit():
        if form.delete.data:
            task_to_delete = Task.query.get(task_id)
            db.session.delete(task_to_delete)
            db.session.commit()
        if form.save.data:
            task_to_update = Task.query.get(task_id)
            task_to_update.text = form.text.data
            task_to_update.owner = form.owner.data
            task_to_update.deadline = form.deadline.data
            task_to_update.done = form.done.data
            db.session.commit()
    return redirect(url_for('home'))


# User actions handling

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)
    # pass


if __name__ == "__main__":
    app.run(
        debug=True,
        host='127.0.0.15',
        port=5200
    )