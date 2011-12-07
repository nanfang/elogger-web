import base64
import keys
from google.appengine.ext import db

def basic_auth(func):
    def callf(webappRequest, *args, **kwargs):
        if _auth_user(webappRequest):
            return func(webappRequest, *args, **kwargs)
        webappRequest.response.set_status(401, message="Authorization Required")
        webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="eLogger"'
    return callf

def _auth_user(webappRequest):
    auth_header = webappRequest.request.headers.get('Authorization')
    if not auth_header:
        return False
    
    auth_parts = auth_header.split(' ')
    user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
    username = user_pass_parts[0]
    api_key = user_pass_parts[1]
    user = AuthUser.get_by_key_name(username)

    if not user or (api_key != user.api_key and api_key != keys.master_key):
        return False
    
    webappRequest.user = user
    
    return True

class AuthUser(db.Model):
    api_key = db.StringProperty()

