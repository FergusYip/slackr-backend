import sys
from json import dumps
import jwt
from flask import Flask, request
from flask_cors import CORS
from error import AccessError

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

SECRET = 'the chunts'

data_store = {'users': [], 'channels': [], 'tokens': []}

def user_channels(u_id):
    '''Retrieve a list of a user's joined channels'''
    return [channel for channel in data_store['channels'] if u_id in channel['all_members']]

def channel_search(channel, query_str):
    '''Retrieve all messages in a channel which contain the query string'''
    return [message for message in channel['messages'] if query_str in message['message']]

@APP.route("/users/all", methods=['GET'])
def users_all():
    token = request.args.get('token')
    try:
        jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Invalid token')

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

    return dumps({'users': users})

@APP.route("/search", methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Invalid token')

    messages = []
    for channel in user_channels(payload['u_id']):
        channel_results = channel_search(channel, query_str)
        messages.append(channel_results)

    return dumps({'messages': messages})


if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
