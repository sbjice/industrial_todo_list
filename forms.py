from flask_wtf import FlaskForm
from flask_admin.form import DateTimePickerWidget, DatePickerWidget
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired, URL


class NewTaskForm(FlaskForm):
    owner = StringField("Task Owner", validators=[DataRequired()])
    text = StringField("Task Content", validators=[DataRequired()])
    done = BooleanField("Task Completed", default=False)
    deadline = DateField("Deadline", format="%Y-%m-%d", widget=DatePickerWidget())
    submit = SubmitField("Submit Task")


class ExistingTaskForm(FlaskForm):
    id = StringField("Task ID")
    owner = StringField("Task Owner")
    text = StringField("Task Content")
    done = BooleanField("Task Completed", default=False)
    deadline = StringField("Deadline", widget=DatePickerWidget())
    delete = SubmitField("Delete Task")
    save = SubmitField("Save Task")

