from __future__ import unicode_literals, print_function, division
from flask import Flask
from elogger.views.tasks import tasks
from elogger.views.eventlogs import eventlogs
from elogger.views.auth import auth
from elogger.views.retro import retro

app = Flask(__name__)

app.register_module(auth)
app.register_module(tasks)
app.register_module(eventlogs)
app.register_module(retro)
