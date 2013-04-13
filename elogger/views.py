from __future__ import unicode_literals, print_function, division
import functools
import json
import logging
import urllib
from datetime import date
from config import secret
from tornado import  httpclient
from tornado.httpclient import HTTPRequest
from tornado.web import RequestHandler, asynchronous, authenticated, HTTPError
from elogger.utils import xtrim
from integration import integration

logger = logging.getLogger(__name__)

def ajax_call(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(self, *args, **kwargs):
        if self.request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            raise HTTPError(400, 'this api support ajax only')
        return view_func(self, *args, **kwargs)

    return _wrapped_view


class SigninHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html", models={})


    @asynchronous
    def post(self, *args, **kwargs):
        username = self.get_argument("username", '')
        password = self.get_argument("password", None)
        if not username:
            self.render("login.html", models=dict(username=username, error='Username can not be empty!'))
            return

        if not password:
            self.render("login.html", models=dict(username=username, error='Password can not be empty!'))
            return
        # TODO move all logic in to Integration
        # TODO support email login
        params = {"username": username, "password": password}

        request = HTTPRequest(
            url='https://api.parse.com/1/login?%s' % urllib.urlencode(params),
            headers={
                "X-Parse-Application-Id": secret.PARSE_APPLICATION_ID,
                "X-Parse-REST-API-Key": secret.PARSE_REST_API_KEY,
            }
        )
        http = httpclient.AsyncHTTPClient()
        http.fetch(request=request, callback=self.on_login)

    def on_login(self, response):
        result = json.loads(response.body)
        if 'username' not in result:
            self.render("login.html", models=dict(error="Invalid Username/Password"))
            return

        user = {
            'userid': result['objectId'],
            'username': result['username'],
            'nickname': result['username'],
            'access_token': result['sessionToken']
        }
        self.set_secure_cookie("user", json.dumps(user))
        self.redirect('/', permanent=True)


class SignupHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html", models=dict())

    @asynchronous
    def post(self, *args, **kwargs):
        self.username = self.get_argument("signupUsername", '')
        self.email = self.get_argument("signupEmail", '')
        password = self.get_argument("signupPassword", '')
        if not self.username:
            self.render("login.html",
                models=dict(username=self.username, email=self.email, error='Username can not be empty!'))
            return

        if not self.email:
            self.render("login.html",
                models=dict(username=self.username, email=self.email, error='Email can not be empty!'))
            return

        if not password:
            self.render("login.html",
                models=dict(username=self.username, email=self.email, error='Password can not be empty!'))
            return

        request = HTTPRequest(
            url='https://api.parse.com/1/users',
            headers={
                "X-Parse-Application-Id": secret.PARSE_APPLICATION_ID,
                "X-Parse-REST-API-Key": secret.PARSE_REST_API_KEY,
                "Content-Type": "application/json",
            },
            method='POST',
            body=json.dumps({
                "username": self.username,
                "password": password,
                "email": self.email
            }),

        )

        http = httpclient.AsyncHTTPClient()

        http.fetch(request=request, callback=self.on_login)

    def on_login(self, response):
        result = json.loads(response.body)
        print(result)
        if response.code != 201:
            error = result.get('error', 'Error to sign up')
            self.render("login.html", models=dict(error=error, username=self.username, email=self.email))
            return

        user = {
            'userid': result['objectId'],
            'username': self.username,
            'nickname': '%s' % self.username,
            'access_token': result['sessionToken']
        }

        self.set_secure_cookie("user", json.dumps(user))
        self.redirect('/', permanent=True)


class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return json.loads(user_json)
        return None


class LogoutHandler(BaseHandler):
    def initialize(self, redirect_url):
        self.redirect_url = redirect_url

    def get(self, *args, **kwargs):
        self.clear_cookie("user")
        self.redirect(self.redirect_url)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class MainHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        user = self.current_user
        today = date.today()
        year = self.get_argument('year', today.year)
        month = self.get_argument('month', today.month)
        self.render('main.html',
            **{'user': user, 'year': year, 'month': month})


class DayLogHandler(BaseHandler):
    @asynchronous
    @authenticated
    @ajax_call
    def get(self, *args, **kwargs):
        user = self.current_user
        year = self.get_argument("year", None)
        month = self.get_argument("month", None) # 1 based
        # TODO check args
        logger.debug('%s-%s' % (year, month))
        integration.get_month_logs(
            userid=user['userid'],
            year=int(year),
            month=int(month),
            callback=self._on_get_logs)

    @asynchronous
    @authenticated
    @ajax_call
    def post(self, *args, **kwargs):
        user = self.current_user
        daylog = json.loads(self.request.body)

        integration.put_day_log(
            id=xtrim(daylog.get('id')),
            userid=user['userid'],
            year=daylog['year'],
            month=daylog['month'],
            day=daylog['day'],
            content=daylog['content'],
            callback=self._on_put_log)

    def _on_put_log(self, id):
        self.write(id)
        self.set_status(200)
        self.finish()

    def _on_get_logs(self, day_logs):
        self.set_status(200)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(day_logs))
        self.finish()


class PreviewHandler(BaseHandler):
    def get(self, *args, **kwargs):
        logger.debug('preview')
        self.render('preview.html')



