from functools import wraps
from flask import Response, request, g
from slackr import token_validation


def auth_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            payload = request.get_json()
        else:
            payload = request.values

        token_payload = token_validation.decode_token(payload.get('token'))
        g.token_payload = token_payload
        return func(*args, **kwargs)

    return decorated_function
