import logging
from google.appengine.ext import db
from google.appengine.ext import webapp
from django.utils import simplejson
from auth import basic_auth

logger = logging.getLogger(__name__)

class DayLog(db.Model):
    day = db.IntegerProperty(required=True)
    month = db.IntegerProperty(required=True)
    year = db.IntegerProperty(required=True)
    content = db.TextProperty()
    plan = db.TextProperty()
    owner = db.StringProperty()

class DayLogHandler(webapp.RequestHandler):
    @basic_auth
    def get(self):
        year = int(self.request.get('year'))
        month = int(self.request.get('month'))
        day_logs = self._get_month_logs(month, year)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(
            simplejson.dumps(
                [{'day': day_log.day,
                  'content': day_log.content,
                  'plan': day_log.plan,
                  } for day_log in day_logs]))

    @basic_auth
    def post(self):
        self._save_day_log(simplejson.loads(self.request.body))
        self.response.set_status(200)

    def _get_month_logs(self, month, year):
        day_logs = db.GqlQuery(
            "SELECT * FROM DayLog WHERE owner = :1 AND year = :2 AND month= :3 ORDER BY day DESC",
            self.user, year, month)
        return day_logs

    def _save_day_log(self, log_dict):
        day_log = DayLog()
        day_log.day = log_dict.get('day')
        day_log.month = log_dict.get('month')
        day_log.year = log_dict.get('year')
        day_log.content = log_dict.get('content')
        day_log.plan = log_dict.get('plan')
        day_log.put()