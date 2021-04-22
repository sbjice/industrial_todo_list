from flask import render_template, redirect, url_for, Blueprint, flash
from tasks.forms import NewTaskForm, ExistingTaskForm
import datetime
from db_interact import Task, db
from utils import create_existing_tasks_forms
from flask_login import current_user


tasks_blueprint = Blueprint(
    'tasks_blueprint',
    __name__,
    template_folder='templates/tasks'
)


@tasks_blueprint.route('/', methods=["GET"])
def home():
    new_task_form = NewTaskForm()
    task_forms = create_existing_tasks_forms()
    return render_template('tasks_index.html', tasks=task_forms, form=new_task_form)


@tasks_blueprint.route('/tasks')
def get_tasks():
    tasks = create_existing_tasks_forms()
    return render_template('tasks_template.html', tasks=tasks)


@tasks_blueprint.route('/new_task', methods=["GET", "POST"])
def new_task():
    form = NewTaskForm()
    if not current_user.is_authenticated:
        flash('You are not logged in to add new tasks. Please Login!')
        return redirect(url_for('auth_blueprint.login'))

    if form.validate_on_submit():
        task = Task(
            text=form.text.data,
            owner=form.owner.data,
            deadline=form.deadline.data if form.deadline.data else str(datetime.date.today()),
            done=form.done.data
        )
        db.session.add(task)
        db.session.commit()
    else:
        return redirect(url_for('tasks_blueprint.home'))
    return redirect(url_for('tasks_blueprint.get_tasks'))


@tasks_blueprint.route('/change_tasks/<int:task_id>', methods=["POST"])
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
    return redirect(url_for('tasks_blueprint.home'))

