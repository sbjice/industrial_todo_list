from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import NewTaskForm, ExistingTaskForm
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


@app.route('/', methods=["GET"])
def home():
    tasks = Task.query.all()
    new_task_form = NewTaskForm()
    task_forms = []
    for task in tasks:
        form = create_form_from_task(task)
        task_forms.append(form)
    return render_template('index.html', tasks=task_forms, form=new_task_form)


@app.route('/tasks', methods=["GET", "POST"])
def get_tasks():
    form = NewTaskForm()
    if form.validate_on_submit():
        print(f"{form.text.data}\n"
              f"{form.owner.data}\n"
              f"{form.deadline.data}\n"
              f"{form.done.data}\n\n")

        new_task = Task(
            text=form.text.data,
            owner=form.owner.data,
            deadline=form.deadline.data if form.deadline.data else str(datetime.date.today()),
            done=form.done.data
        )

        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', form=form)


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


if __name__ == "__main__":
    app.run(
        debug=True,
        host='127.0.0.15',
        port=5200
    )