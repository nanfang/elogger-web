import json
import logging
import urllib
import time
import binascii
import uuid
import tornado
from tornado.auth import  OAuthMixin, _oauth10a_signature, _oauth_signature
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.util import bytes_type, b

from tornado.web import RequestHandler, asynchronous, authenticated
from pycket.session import SessionMixin


logger = logging.getLogger(__name__)


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
        http.fetch(self._oauth_verify_url(access_token), self._on_auth)

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

class WeiboHandler(tornado.web.RequestHandler, WeiboMixin, SessionMixin):
    def initialize(self, api_key, api_secret, auth_callback, auth_success):
        self.api_key=api_key
        self.api_secret=api_secret
        self.auth_callback=auth_callback
        self.auth_success=auth_success

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, response):
        if not response:
            raise tornado.web.HTTPError(500, "Weibo auth failed")
        user_info = json.loads(response.body)
        self.session.set('user', user_info)
        self.redirect(self.auth_success, permanent=True)

class BaseHandler(RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('user')

class MainHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render("main.html", **{'user_info':self.session.get('user')})


