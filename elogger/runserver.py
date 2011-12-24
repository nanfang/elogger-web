import logging
import os

import tornado.ioloop
import tornado.web
from elogger.views import MainHandler

logger = logging.getLogger(__name__)

settings = {
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "81iETzKXUAGaYckL5gEmGeJJFuYh8EQnp2XdTP1o/Vo=",
    # TODO config it
    'debug': True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)

if __name__ == "__main__":
    port = 8080
    print('start server, listening %s' % port)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()