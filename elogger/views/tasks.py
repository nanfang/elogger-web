from __future__ import unicode_literals, print_function, division
from flask import  request, render_template

from flask import Module

from elogger.database import redis

tasks = Module(__name__)

@frontend.route("/favicon.ico")
def favicon():
    return frontend.send_static_file("terry_turtle.png")
#
#@tasks.route('/<user>')
#def main(user):
#    return render_template('main.html', user=user)

@tasks.route('/<user>/tasks')
def index(user):
    return render_template('tasks.html', user=user, **redis.hgetall('%s:tasks' % user))

@tasks.route('/<user>/tasks', methods=['POST'])
def save(user):
    redis.hmset('%s:tasks' % user, request.form)
    return ''
