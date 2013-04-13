import logging
import os
import sys
import tornado.ioloop
import tornado.web
from elogger.views import MainHandler, SigninHandler, PreviewHandler, DayLogHandler, LogoutHandler, SignupHandler
from elogger import settings

DEFAULT_PORT = 8000
logger = logging.getLogger(__name__)

application_settings = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "81iETzKXUAGaYckL5gEmGeJJFuYh8EQnp2XdTP1o/Vo=",
    'debug': settings.DEBUG,
    "login_url": "/sign-in",
    }

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/preview', PreviewHandler),
    (r'/sign-in', SigninHandler),
    (r'/sign-up', SignupHandler),
    (r'/logout', LogoutHandler, {'redirect_url':'/sign-in'}),
    (r'/logs', DayLogHandler),

], **application_settings)

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    logging.getLogger().setLevel(settings.LOG_LEVEL)
    print('start server, listening %s' % port)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()