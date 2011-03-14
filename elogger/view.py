from __future__ import unicode_literals, print_function, division
from elogger.application import app

from flask import Flask, request, render_template
from flask.helpers import jsonify

from elogger.database import redis


@app.route('/<user>')
def index(user):
    return render_template('main.html', user=user)

@app.route('/<user>/tasks')
def tasks(user):
    return render_template('tasks.html', user=user, **redis.hgetall('%s:tasks' % user))

@app.route('/<user>/event-log')
def event_log(user):
    return render_template('event-log.html', user=user)

@app.route('/<user>/event-log/<int:year>')
def annual_log(user,year):
    return jsonify(redis.hgetall('%s:event-log:%s' % (user, year)))

@app.route('/<user>/event-log/<int:year>', methods=['POST', 'PUT'])
def save_log(user, year):
    redis.hset('%s:event-log:%s' % (user, year), request.form['element_id'], request.form['update_value'])
    return '<pre>' + request.form['update_value'] + '</pre>'

@app.route('/<user>/tasks', methods=['POST'])
def save_tasks(user):
    print('post:'+user)
    redis.hmset('%s:tasks' % user, request.form)
    return ''

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("terry_turtle.png")