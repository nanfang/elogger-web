from __future__ import unicode_literals, print_function, division
from flask import Flask
from elogger.views.notes import notes
from elogger.views.elogs import elogs
from elogger.views.auth import auth
from elogger.views.retro import retro
from elogger.views.todos import todos

app = Flask(__name__)

app.register_module(auth)
app.register_module(notes)
app.register_module(elogs)
app.register_module(retro)
app.register_module(todos,url_prefix='/todos')
