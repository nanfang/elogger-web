from __future__ import unicode_literals, print_function, division
from flask import  request, session,render_template
from flask.helpers import jsonify
from flask import Module

from elogger.views.auth import requires_auth
from elogger.database import redis

eventlogs = Module(__name__)

@eventlogs.route('/event-log')
@requires_auth
def event_log():
    return render_template('event-log.html', user=session['username'])

@eventlogs.route('/event-log/<int:year>')
@requires_auth
def annual_log(year):
    return jsonify(redis.hgetall('%s:event-log:%s' % (session['username'], year)))

@eventlogs.route('/event-log/<int:year>', methods=['POST', 'PUT'])
@requires_auth
def save_log(year):
    redis.hset('%s:event-log:%s' % (session['username'], year), request.form['element_id'], request.form['update_value'])
    return '<pre>' + request.form['update_value'] + '</pre>'
