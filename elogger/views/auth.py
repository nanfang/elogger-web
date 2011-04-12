from __future__ import unicode_literals, print_function, division
from functools import wraps
from flask import   render_template

from flask import Module
from flask import  session, redirect, url_for, request

from elogger.database import redis

auth = Module(__name__)


@auth.route('/')
def index():
    return redirect(url_for('todos.index'))

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        login_name = request.form['username']
        password = request.form['password']

        if login_name and password == redis.get('%s:password' % login_name):
            session['username'] = request.form['username']
            return redirect(url_for('todos.index'))

    return render_template('sign-in.html')


@auth.route('/sign-out')
def sign_out():
    # remove the username from the session if its there
    session.pop('username', None)
    return redirect(url_for('sign_in'))

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return render_template('sign-in.html')

        return f(*args, **kwargs)
    return decorated