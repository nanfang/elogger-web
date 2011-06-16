from __future__ import unicode_literals, print_function, division
import json
from flask import request, session, render_template, Module
from elogger.views.auth import requires_auth
from elogger.database import redis

todos = Module(__name__)

TOP_NUM = 10

@todos.route('')
@requires_auth
def index():
    return render_template('todos.html')


@todos.route('/tops')
@requires_auth
def tops():
    return json.dumps(_top())


@todos.route('', methods=['POST'])
@requires_auth
def create():
    todo = request.form['todo']
    size = _count()

    operation = 'I'
    update_list = 'coming'
    title = todo
    if size < TOP_NUM:
        operation = 'A'
        update_list= 'tops'

    # persistence
    return json.dumps({'op': operation, 'l': update_list, 't': title})


def _next_id():
    return redis.incr('%s:todos:id' % session['username'])


def _top():
    return redis.zrange(_key(), 0, TOP_NUM - 1, True, True)


def _count():
    return redis.zcard(_key())


def _key():
    return '%s:todos.ranking' % session['username']

