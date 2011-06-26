from __future__ import unicode_literals, print_function, division
import json
from flask import request, session, render_template, Module
from elogger.views.auth import requires_auth
from elogger.repository import todo

todos = Module(__name__)

OP_APPEND='A'
OP_PREPEND='P'

TARGET_TOPS='T'
TARGET_COMINGS='C'

@todos.route('')
@requires_auth
def index():
    return render_template('todos.html')

@todos.route('/tops')
@requires_auth
def tops():
    return json.dumps(todo.tops(session['username']))

@todos.route('/comings')
@requires_auth
def comings():
    return json.dumps(todo.comings(session['username']))

@todos.route('', methods=['POST'])
@requires_auth
def create():
    new_todo=todo.new_todo(session['username'], request.form['todo']).save()
    operation, update_target = (OP_APPEND, TARGET_TOPS) if new_todo.is_in_tops() else (OP_PREPEND, TARGET_COMINGS)
    return json.dumps({'op': operation, 't': update_target, 'todo': {'t':new_todo.title,'s':new_todo.score, 'id':new_todo.id}})

