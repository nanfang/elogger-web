import logging

import tornado.ioloop
import tornado.web

logger = logging.getLogger(__name__)

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("preview.html")
