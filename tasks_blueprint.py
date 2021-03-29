from flask import render_template, redirect, url_for,Blueprint
from forms import NewTaskForm, ExistingTaskForm, RegisterForm, LoginForm
import datetime
from db_interact import Task, db
from utils import create_existing_tasks_forms

tasks_blueprint = Blueprint(
    'tasks_blueprint',
    __name__,
    template_folder='templates'
)


@tasks_blueprint.route('/', methods=["GET"])
def home():
    new_task_form = NewTaskForm()
    task_forms = create_existing_tasks_forms()
    return render_template('index.html', tasks=task_forms, form=new_task_form)


@tasks_blueprint.route('/tasks')
def get_tasks():
    tasks = create_existing_tasks_forms()
    return render_template('tasks.html', tasks=tasks)


@tasks_blueprint.route('/new_task', methods=["POST"])
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
    return redirect(url_for('home'))


# User actions handling

@tasks_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@tasks_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
