import logging
from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson
from auth import basic_auth

logger=logging.getLogger(__name__)

class Retro(db.Model):
    goal = db.TextProperty()
    good = db.TextProperty()
    bad = db.TextProperty()
    action = db.TextProperty()
    
    owner = db.StringProperty()
    retro_on = db.StringProperty()

    created_on = db.DateTimeProperty(auto_now_add=True)

class RetroHandler(webapp.RequestHandler):
    @basic_auth
    def get(self):
        retros = db.GqlQuery("SELECT * FROM Retro WHERE owner = :1 ORDER BY retro_on DESC, created_on DESC", owner=self.user.key_name)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(
                simplejson.dumps(
                        [{
                          'id': retro.key().id(),
                          'goal': retro.goal or '',
                          'good': retro.good or '',
                          'bad': retro.bad or '',
                          'action': retro.action or '',
                          'retro_on': retro.retro_on or '',
                         } for retro in retros]))

    @basic_auth
    def post(self):
        logger.info(self.request.body)
        self._add_retro(simplejson.loads(self.request.body))
        self.response.set_status(202)
        self.response.out.write("")

    def _add_retro(self, retro_dict):
        retro=Retro()
        retro.goal=retro_dict.get('goal')
        retro.good=retro_dict.get('good')
        retro.bad=retro_dict.get('bad')
        retro.action=retro_dict.get('action')
        retro.owner=self.user.key_name
        retro.retro_on=retro_dict.get('retro_on')
        retro.put()
