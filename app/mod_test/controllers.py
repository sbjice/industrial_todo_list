from flask import (Blueprint, render_template, url_for)

mod = Blueprint('test', __name__, url_prefix='/')


@mod.route('/', methods=['GET', 'POST'])
def home():
    return render_template('test.html')
