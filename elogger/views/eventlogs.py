from __future__ import unicode_literals, print_function, division
from flask import  request, render_template

from flask.helpers import jsonify
from flask import Module

from elogger.database import redis

eventlogs = Module(__name__)


@eventlogs.route('/<user>/event-log')
def event_log(user):
    return render_template('event-log.html', user=user)

@eventlogs.route('/<user>/event-log/<int:year>')
def annual_log(user,year):
    return jsonify(redis.hgetall('%s:event-log:%s' % (user, year)))

@eventlogs.route('/<user>/event-log/<int:year>', methods=['POST', 'PUT'])
def save_log(user, year):
    redis.hset('%s:event-log:%s' % (user, year), request.form['element_id'], request.form['update_value'])
    return '<pre>' + request.form['update_value'] + '</pre>'
