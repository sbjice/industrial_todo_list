from auth.forms import RegisterForm, LoginForm
from flask import render_template, redirect, url_for, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash

from db_interact import User, db
from flask_login import login_user, logout_user, current_user, LoginManager, login_required


auth_blueprint = Blueprint(
    'auth_blueprint',
    __name__,
    template_folder='templates/auth'
)


@auth_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('The User with given email already exists. Please Login!')
            return redirect(url_for('auth_blueprint.login'))
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)

    return render_template('auth_register.html', form=form)


@auth_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash(u'Sign Up or Sign In', category='error')
            return redirect(url_for('auth_blueprint.register'))
        if check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('tasks_blueprint.get_tasks'))
        else:
            flash(u'Invalid password provided', 'error')
            return redirect(url_for('auth_blueprint.login'))

    return render_template('auth_login.html', form=form)


@auth_blueprint.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))
