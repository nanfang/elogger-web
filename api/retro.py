from __future__ import unicode_literals, print_function, division

import json
import logging
from google.appengine.ext import db

from google.appengine.ext import webapp

logger=logging.getLogger(__name__)

class Retro(db.Model):
    goal = db.TextProperty()
    good = db.TextProperty()
    bad = db.TextProperty()
    action = db.TextProperty()
    
    owner = db.StringProperty(multiline=False)
    retro_on = db.StringProperty(multiline=False)

    created_on = db.DateTimeProperty(auto_now_add=True)

class RetroHandler(webapp.RequestHandler):
    def get(self):
        owner=self.request.get('owner')
        if owner:
            retros = db.GqlQuery("SELECT * FROM Retro WHERE owner = :1 ORDER BY retro_on DESC, created_on DESC", owner)
        else:
            retros = db.GqlQuery("SELECT * FROM Retro ORDER BY retro_on DESC, created_on DESC")

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(
                json.dumps(
                        [{'goal': retro.goal or '',
                          'good': retro.good or '',
                          'bad': retro.bad or '',
                          'action': retro.action or '',
                          'retro_on': retro.retro_on or '',
                          'owner': retro.owner,
                         } for retro in retros]))

    def post(self):
        logger.info(self.request.body)
        self._add_retro(json.loads(self.request.body))
        self.response.set_status(202)
        self.response.out.write("")

    def _add_retro(self, retro_dict):
        retro=Retro()
        retro.goal=retro_dict.get('goal')
        retro.good=retro_dict.get('good')
        retro.bad=retro_dict.get('bad')
        retro.action=retro_dict.get('action')
        retro.owner=retro_dict.get('owner')
        retro.retro_on=retro_dict.get('retro_on')
        retro.put()
