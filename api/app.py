from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import json

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('We are waiting to open this service...')


class WeelyThink(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(
                json.dumps({'2010-04-16': {'goals': 'test', 'ideas': '', 'assignments': '', 'actions': ''}}))


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/weekly-think', WeelyThink), ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()