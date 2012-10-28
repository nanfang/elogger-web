import logging
import os
import sys
import tornado.ioloop
import tornado.web
from elogger.views import MainHandler, SigninHandler, WeiboHandler, PreviewHandler, DayLogHandler, LogoutHandler, SignupHandler
from elogger import settings
from elogger.config.secret import WEIBO_API_KEY, WEIBO_API_SECRET

DEFAULT_PORT = 8000
logger = logging.getLogger(__name__)

application_settings = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "81iETzKXUAGaYckL5gEmGeJJFuYh8EQnp2XdTP1o/Vo=",
    'debug': settings.DEBUG,
    "login_url": "/sign-in",
    'pycket': {
        'engine': 'redis',
        'storage': {
            'host': 'localhost',
            'port': 6379,
            'db_sessions': 10,
            'db_notifications': 11,
            },
        'cookies': {
            'expires_days': 30,
            },
        },
    }

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/preview', PreviewHandler),
    (r'/sign-in', SigninHandler),
    (r'/sign-up', SignupHandler),
    (r'/logout', LogoutHandler, {'redirect_url':'/sign-in'}),
    (r'/logs', DayLogHandler),
    (r'/auth/weibo', WeiboHandler, {'api_key': WEIBO_API_KEY,
                                    'api_secret': WEIBO_API_SECRET,
                                    'auth_callback': '/auth/weibo',
                                    'auth_success': '/',
    }),

], **application_settings)

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    logging.getLogger().setLevel(settings.LOG_LEVEL)
    print('start server, listening %s' % port)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()