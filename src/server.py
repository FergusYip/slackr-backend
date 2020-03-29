'''Backend server file for slackr'''
import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from data_store import autosave

# Route implementations
import admin
import auth
import channel
import channels
import message as msg
import other
import standup
import user
import workspace

AUTOSAVE_ENABLED = True
DEBUG_MODE = not AUTOSAVE_ENABLED  # Do not change this line


def defaultHandler(err):
    '''Default handler for errors'''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


@APP.route('/admin/userpermission/change', methods=['POST'])
def route_admin_userpermission_change():
    '''Flask route for /admin/userpermission/change'''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return dumps(admin.admin_userpermission_change(token, u_id, permission_id))


@APP.route("/auth/register", methods=['POST'])
def route_auth_register():
    '''Flask route for /auth/register'''
    payload = request.get_json()
    email = payload.get('email')
    password = payload.get('password')
    name_first = payload.get('name_first')
    name_last = payload.get('name_last')
    return dumps(auth.auth_register(email, password, name_first, name_last))


@APP.route("/auth/login", methods=['POST'])
def route_auth_login():
    '''Flask route for /auth/login'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    return dumps(auth.auth_login(email, password))


@APP.route("/auth/logout", methods=['POST'])
def route_auth_logout():
    '''Flask route for /auth/logout'''
    payload = request.get_json()
    token = payload['token']
    return dumps(auth.auth_logout(token))


@APP.route("/channel/invite", methods=['POST'])
def route_channel_invite():
    '''
    Flask route to implement channel_invite function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel.channel_invite(token, channel_id, u_id))


@APP.route("/channel/details", methods=['GET'])
def route_channel_details():
    '''
    Flask route to implement channel_invite function.
    '''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    return dumps(channel.channel_details(token, channel_id))


@APP.route("/channel/messages", methods=['GET'])
def route_channel_messages():
    '''
    Flask route for channel_messages function.
    '''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    start = request.values.get('start')
    return dumps(channel.channel_messages(token, channel_id, start))


@APP.route("/channel/leave", methods=['POST'])
def route_channel_leave():
    '''
    Flask route to implement channel_leave function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(channel.channel_leave(token, channel_id))


@APP.route("/channel/join", methods=['POST'])
def route_channel_join():
    '''
    Flask route for channel_join function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(channel.channel_join(token, channel_id))


@APP.route("/channel/addowner", methods=['POST'])
def route_channel_addowner():
    '''
    Flask route for channel_addowner function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel.channel_addowner(token, channel_id, u_id))


@APP.route("/channel/removeowner", methods=['POST'])
def route_channel_removeowner():
    '''
    Implementing removeowner function by removing user from channel['owner_members']
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel.channel_removeowner(token, channel_id, u_id))


@APP.route("/channels/list", methods=['GET'])
def route_channels_list():
    '''Flask route for /channels/list'''
    token = request.values.get('token')
    return dumps(channels.channels_list(token))


@APP.route("/channels/listall", methods=['GET'])
def route_channels_listall():
    '''Flask route for /channels/listall'''
    token = request.values.get('token')
    return dumps(channels.channels_listall(token))


@APP.route("/channels/create", methods=['POST'])
def route_channels_create():
    '''Flask route for /channels/create'''
    payload = request.get_json()
    token = payload.get('token')
    name = payload.get('name')
    is_public = payload.get('is_public')
    return dumps(channels.channels_create(token, name, is_public))


@APP.route("/message/send", methods=['POST'])
def route_message_send():
    '''
    Flask route to call the message_send function.
    '''

    payload = request.get_json()

    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']

    return dumps(msg.message_send(token, channel_id, message))


@APP.route("/message/remove", methods=['DELETE'])
def route_message_remove():
    '''
    Flask route to call the message_remove function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(msg.message_remove(token, message_id))


@APP.route("/message/edit", methods=['PUT'])
def route_message_edit():
    '''
    Flask route to call the message_edit function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])
    new_message = payload['message']

    return dumps(msg.message_edit(token, message_id, new_message))


@APP.route("/message/sendlater", methods=['POST'])
def route_message_sendlater():
    '''
    Flask route to call the message_sendlater function.
    '''

    payload = request.get_json()

    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    time_sent = int(payload['time_sent'])

    return dumps(msg.message_sendlater(token, channel_id, message, time_sent))


@APP.route("/message/react", methods=['POST'])
def route_message_react():
    '''
    Flask route to call the message_react function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = int(payload['react_id'])

    return dumps(msg.message_react(token, message_id, react_id))


@APP.route("/message/unreact", methods=['POST'])
def route_message_unreact():
    '''
    Flask route to call the message_unreact function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = int(payload['react_id'])

    return dumps(msg.message_unreact(token, message_id, react_id))


@APP.route("/message/pin", methods=['POST'])
def route_message_pin():
    '''
    Flask route to call the message_pin function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(msg.message_pin(token, message_id))


@APP.route("/message/unpin", methods=['POST'])
def route_message_unpin():
    '''
    Flask route to call the message_unpin function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(msg.message_unpin(token, message_id))


@APP.route("/users/all", methods=['GET'])
def route_users_all():
    '''Flask route for /users/all'''
    token = request.values.get('token')
    return dumps(other.users_all(token))


@APP.route("/search", methods=['GET'])
def route_search():
    '''Flask route for /search'''
    token = request.values.get('token')
    query_str = request.values.get('query_str')
    return dumps(other.search(token, query_str))


@APP.route("/standup/start", methods=['POST'])
def route_standup_start():
    '''Flask route for /standup/start'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    length = payload.get('length')
    return dumps(standup.standup_start(token, channel_id, length))


@APP.route("/standup/active", methods=['GET'])
def route_standup_active():
    '''Flask route for /standup/active'''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    return dumps(standup.standup_active(token, channel_id))


@APP.route("/standup/send", methods=['POST'])
def route_standup_send():
    '''Flask route for /standup/send'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    return dumps(standup.standup_send(token, channel_id, message))


@APP.route('/user/profile', methods=['GET'])
def route_user_profile():
    '''
    Flask route to call the user_profile function.
    '''

    token = request.values.get('token')
    target_user = int(request.values.get('u_id'))

    return dumps(user.user_profile(token, target_user))


@APP.route('/user/profile/setname', methods=['PUT'])
def route_user_profile_setname():
    '''
    Flask route to call the user_profile_setname function.
    '''

    payload = request.get_json()

    token = payload['token']
    first_name = payload['name_first']
    last_name = payload['name_last']

    return dumps(user.user_profile_setname(token, first_name, last_name))


@APP.route('/user/profile/setemail', methods=['PUT'])
def route_user_profile_setemail():
    '''
    Flask route to call the user_profile_setemail function.
    '''

    payload = request.get_json()

    token = payload['token']
    desired_email = payload['email']

    return dumps(user.user_profile_setemail(token, desired_email))


@APP.route('/user/profile/sethandle', methods=['PUT'])
def route_user_profile_sethandle():
    '''
    Flask route to call the user_profile_sethandle function.
    '''

    payload = request.get_json()

    token = payload['token']
    desired_handle = payload['handle_str']

    return dumps(user.user_profile_sethandle(token, desired_handle))


@APP.route("/workspace/reset", methods=['POST'])
def route_workspace_reset():
    ''' Flask route for /workspace/reset in slackr'''
    return dumps(workspace.workspace_reset())


if __name__ == "__main__":
    if AUTOSAVE_ENABLED:
        autosave()
    APP.run(debug=DEBUG_MODE,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
