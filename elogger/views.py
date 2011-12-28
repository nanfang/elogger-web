import logging

from tornado.web import RequestHandler, authenticated
from pycket.session import SessionMixin

logger = logging.getLogger(__name__)

class BaseHandler(RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('user')

class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")

class WeiboAuthHandler(RequestHandler):
    pass

class MainHandler(BaseHandler):
#    @authenticated
    def get(self, *args, **kwargs):
        self.render("preview.html")
