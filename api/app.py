import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from api.daylog import DayLogHandler
from retro import RetroHandler

logger = logging.getLogger(__name__)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('We are waiting to open this service...')

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/retros', RetroHandler),
    ('/elog', DayLogHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()