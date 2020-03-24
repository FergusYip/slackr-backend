import sys
from json import dumps
from flask import request, Blueprint
from data_store import data_store
from token_validation import decode_token
from helpers import user_channels, channel_search

OTHER = Blueprint('other', __name__)


@OTHER.route("/users/all", methods=['GET'])
def route_users_all():
    token = request.values.get('token')
    return dumps(users_all(token))


@OTHER.route("/search", methods=['GET'])
def route_search():
    token = request.values.get('token')
    query_str = request.values.get('query_str')
    return dumps(search(token, query_str))


def users_all(token):
    decode_token(token)

    users = []
    for user in data_store['users']:
        user_dict = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
        }
        users.append(user_dict)

    return {'users': users}


def search(token, query_str):
    token_payload = decode_token(token)

    messages = []
    for channel in user_channels(token_payload['u_id']):
        channel_results = channel_search(channel, query_str)
        messages.append(channel_results)

    return {'messages': messages}


if __name__ == "__main__":
    pass
