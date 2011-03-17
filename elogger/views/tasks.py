from __future__ import unicode_literals, print_function, division
from flask import  session, request, render_template

from flask import Module

from elogger.database import redis
from elogger.views.auth import requires_auth

tasks = Module(__name__)

@tasks.route("/favicon.ico")
def favicon():
    return tasks.send_static_file("favicon.png")
#
#@tasks.route('/<user>')
#def main(user):
#    return render_template('main.html', user=user)

@tasks.route('/tasks')
@requires_auth
def index():
    return render_template('tasks.html', user=session['username'], **redis.hgetall('%s:tasks' % session['username']))

@tasks.route('/tasks', methods=['POST'])
@requires_auth
def save():
    redis.hmset('%s:tasks' % session['username'], request.form)
    return ''
