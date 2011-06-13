from __future__ import unicode_literals, print_function, division
from flask import  request, session, render_template
from flask.helpers import jsonify
from flask import Module
from elogger.common.utils import xstr
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
    return jsonify(redis.hgetall(_event_log_key(year)))


@elogs.route('/logs/<int:year>', methods=['POST', 'PUT'])
@requires_auth
def save_log(year):
    redis.hset(_event_log_key(year), request.form['element_id'], request.form['update_value'])
    return '<pre>' + request.form['update_value'] + '</pre>'


@elogs.route('/logs/<int:year>/<string:date>', methods=['POST', 'PUT', 'GET'])
@requires_auth
def daily_log(year, date):
    key= _event_log_key(year)
    def get():
        return xstr(redis.hget(key, date))

    def update():
        redis.hset(key, date, request.data)
        return ''

    return {'GET': get,
            'POST': update,
            'PUT': update}[request.method]


def _event_log_key(year):
    return '%s:event-log:%s' % (session['username'], year)

