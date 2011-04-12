from __future__ import unicode_literals, print_function, division
from flask import    render_template

from flask import Module

from elogger.views.auth import requires_auth

weeklythink = Module(__name__)


@weeklythink.route('/weekly-think')
@requires_auth
def index():
    return render_template('weekly-think.html')
