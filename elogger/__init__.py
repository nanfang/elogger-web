from __future__ import unicode_literals, print_function, division
from flask import Flask
from elogger.views.notes import notes
from elogger.views.logs import logs
from elogger.views.auth import auth
from elogger.views.retro import retro

app = Flask(__name__)

app.register_module(auth)
app.register_module(notes)
app.register_module(logs)
app.register_module(retro)
