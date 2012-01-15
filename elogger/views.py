from __future__ import unicode_literals, print_function, division
import functools
import json
import logging
import urllib
import time
import binascii
import uuid
from tornado import escape, httpclient
from tornado.auth import  OAuthMixin, _oauth10a_signature, _oauth_signature
from tornado.web import RequestHandler, asynchronous, authenticated, HTTPError
from pycket.session import SessionMixin

from integration import integration

logger = logging.getLogger(__name__)

def ajax_call(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(self, *args, **kwargs):
        if self.request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            raise HTTPError(400, 'this api support ajax only')
        return view_func(self, *args, **kwargs)

    return _wrapped_view


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")



class WeiboMixin(OAuthMixin):
    _OAUTH_REQUEST_TOKEN_URL = "http://api.t.sina.com.cn/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "http://api.t.sina.com.cn/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "http://api.t.sina.com.cn/oauth/authorize"
    _OAUTH_VERIFY_URL = "http://api.t.sina.com.cn/account/verify_credentials.json"


    def authenticate_redirect(self):
        http = httpclient.AsyncHTTPClient()
        http.fetch(self._oauth_request_token_url(self.auth_callback),
            self.async_callback(self._on_request_token, self._OAUTH_AUTHORIZE_URL, None))

    def api_request(self, path, callback, access_token=None,
                        post_args=None, **args):
        url = "https://api.weibo.com/2" + path + ".json"
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args: url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_api_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_api_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error,
                response.request.url)
            callback(None)
            return
        callback(escape.json_decode(response.body))

    def _oauth_consumer_token(self):
        return dict(key=self.api_key, secret=self.api_secret)

    def _oauth_get_user(self, access_token, callback):
        http = httpclient.AsyncHTTPClient()
        http.fetch(self._oauth_verify_url(access_token), self.async_callback(self._on_auth, access_token))

    def _oauth_verify_url(self, access_token):
        consumer_token = self._oauth_consumer_token()
        url = self._OAUTH_VERIFY_URL
        args = dict(
            oauth_consumer_key=consumer_token["key"],
            oauth_token=access_token["key"],
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp=str(int(time.time())),
            oauth_nonce=binascii.b2a_hex(uuid.uuid4().bytes),
            oauth_version=getattr(self, "_OAUTH_VERSION", "1.0a"),
        )

        if getattr(self, "_OAUTH_VERSION", "1.0a") == "1.0a":
            signature = _oauth10a_signature(consumer_token, "GET", url, args, access_token)
        else:
            signature = _oauth_signature(consumer_token, "GET", url, args, access_token)

        args["oauth_signature"] = signature
        return url + "?" + urllib.urlencode(args)


    def _parse_user_response(self, callback, user):
        if user:
            user["username"] = user["screen_name"]
        callback(user)

class WeiboHandler(RequestHandler, WeiboMixin, SessionMixin):
    def initialize(self, api_key, api_secret, auth_callback, auth_success):
        self.api_key=api_key
        self.api_secret=api_secret
        self.auth_callback=auth_callback
        self.auth_success=auth_success

    @asynchronous
    def get(self, *args, **kwargs):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, access_token, response):
        if not response:
            raise HTTPError(500, "Weibo auth failed")
        user_info = json.loads(response.body)

        user = {
            'username':'weibo/%s' %user_info['domain'],
            'nickname':user_info['name'],
            'access_token':access_token
        }

        def on_register():
            self.session.set('user', user)
            self.redirect(self.auth_success, permanent=True)

        integration.register_user(user, on_register)

class BaseHandler(RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('user')

class LogoutHandler(BaseHandler):
    def initialize(self, redirect_url):
        self.redirect_url=redirect_url

    def get(self, *args, **kwargs):
        self.session.delete('user')
        self.redirect(self.redirect_url)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class MainHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        user = self.current_user
        self.render('main.html',
            **{'user': user})

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
            username=user['username'],
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
            username=user['username'],
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



