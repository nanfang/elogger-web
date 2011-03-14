from __future__ import unicode_literals, print_function, division

from flask import Flask, request, render_template
from flask.helpers import jsonify

from elogger.database import redis

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



if __name__ == '__main__':
    app.debug = True
    app.run()

