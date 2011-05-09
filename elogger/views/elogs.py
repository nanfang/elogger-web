from __future__ import unicode_literals, print_function, division
from flask import  request, session,render_template
from flask.helpers import jsonify
from flask import Module

from elogger.views.auth import requires_auth
from elogger.database import redis

elogs = Module(__name__)

@elogs.route('/logs')
@requires_auth
def index():
    return render_template('elogs.html', user=session['username'])

@elogs.route('/logs/<int:year>')
@requires_auth
def annual_log(year):
    return jsonify(redis.hgetall('%s:event-log:%s' % (session['username'], year)))

@elogs.route('/logs/<int:year>', methods=['POST', 'PUT'])
@requires_auth
def save_log(year):
    redis.hset('%s:event-log:%s' % (session['username'], year), request.form['element_id'], request.form['update_value'])
    return '<pre>' + request.form['update_value'] + '</pre>'
