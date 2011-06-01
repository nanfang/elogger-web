from __future__ import unicode_literals, print_function, division
import json
from httplib2 import Http

from flask import Module, request, session, render_template, redirect, url_for

from elogger.views.auth import requires_auth
from elogger.config import config

retro = Module(__name__)

retro_api = config.get('services', 'api') + '/retros'
h = Http(str(".cache"))

@retro.route('/retro')
@requires_auth
def index():
    resp, content = h.request(str(retro_api + '?owner=' + session['username']), str('GET'))
    return render_template('retro.html', retros=json.loads(content))


@retro.route('/retro', methods=['POST'])
@requires_auth
def save():
    body = dict(
        goal=request.form['goal'],
        good=request.form['good'],
        bad=request.form['bad'],
        action=request.form['action'],
        retro_on=request.form['retro_on'],
        owner=session['username'],
        )

    h.request(retro_api, "POST",
              body=json.dumps(body),
              headers={'content-type': 'application/json'})

    return redirect(url_for('retro.index'))
