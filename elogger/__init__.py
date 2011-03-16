from __future__ import unicode_literals, print_function, division
from flask import Flask
from elogger.views.tasks import tasks
from elogger.views.eventlogs import eventlogs

app = Flask(__name__)
app.register_module(tasks)
app.register_module(eventlogs)

