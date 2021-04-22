from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired


class NewTaskForm(FlaskForm):
    owner = StringField("Task Owner", validators=[DataRequired()])
    text = StringField("Task Content", validators=[DataRequired()])
    done = BooleanField("Task Completed", default=False)
    deadline = DateField("Deadline", format="%Y-%m-%d")
    submit = SubmitField("Create Task")


class ExistingTaskForm(NewTaskForm):
    id = StringField("Task ID")
    delete = SubmitField("Delete Task")
    save = SubmitField("Save Task")
