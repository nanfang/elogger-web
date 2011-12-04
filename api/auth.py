import base64

def basic_auth(func):
    def callf(webappRequest, *args, **kwargs):
        # Parse the header to extract a user/password combo.
        # We're expecting something like "Basic XZxgZRTpbjpvcGVuIHYlc4FkZQ=="
        auth_header = webappRequest.request.headers.get('Authorization')

        if auth_header == None:
            webappRequest.response.set_status(401, message="Authorization Required")
            webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="eLogger"'
        else:
            # Isolate the encoded user/passwd and decode it
            auth_parts = auth_header.split(' ')
            user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
            user_arg = user_pass_parts[0]
            pass_arg = user_pass_parts[1]

            # TODO use user name and api_key
            if user_arg != "elogger" or pass_arg != "nanfang":
                webappRequest.response.set_status(401, message="Authorization Required")
                webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="eLogger"'
            else:
                return func(webappRequest, *args, **kwargs)

    return callf