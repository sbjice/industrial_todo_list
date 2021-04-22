from db_interact import Task
import datetime
from tasks.tasks import ExistingTaskForm


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
