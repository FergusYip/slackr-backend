from json import dumps

from flask import Blueprint, request

from slackr.controllers import other
from slackr.middleware import auth_middleware

OTHER_ROUTE = Blueprint('other', __name__)


@OTHER_ROUTE.route("/users/all", methods=['GET'])
@auth_middleware
def route_users_all():
    '''Flask route for /users/all'''
    token = request.values.get('token')
    return dumps(other.users_all(token))


@OTHER_ROUTE.route("/search", methods=['GET'])
@auth_middleware
def route_search():
    '''Flask route for /search'''
    token = request.values.get('token')
    query_str = request.values.get('query_str')
    return dumps(other.search(token, query_str))
