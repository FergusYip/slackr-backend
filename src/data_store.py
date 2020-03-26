import threading
import pickle
from datetime import datetime
import helpers

SECRET = 'the chunts'


class User:
    def __init__(self, email, password, name_first, name_last):
        self.u_id = helpers.generate_u_id()
        self.email = email
        self.password = helpers.hash_pw(password)
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = helpers.generate_handle(name_first, name_last)
        self.permission_id = helpers.default_permission()
        self.channels = []
        self.messages = []
        self.reacts = []

    def set_email(self, email):
        self.email = email

    def set_name(self, name_first, name_last):
        self.name_first = name_first
        self.name_last = name_last

    def change_password(self, password):
        self.password = helpers.hash_pw(password)

    def set_handle(self, handle_str):
        self.handle_str = handle_str

    def change_permission(self, permission_id):
        self.permission_id = permission_id

    @property
    def profile(self):
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
        }

    @property
    def id_names(self):
        return {
            'u_id': self.u_id,
            'name_first': self.name_first,
            'name_last': self.name_last
        }

    def add_channel(self, channel):
        self.channels.append(channel)

    def remove_channel(self, channel):
        self.channels.remove(channel)

    def add_message(self, message):
        self.messages.append(message)

    def remove_message(self, message):
        self.messages.remove(message)

    def add_react(self, react):
        self.reacts.append(react)

    def remove_react(self, react):
        self.reacts.remove(react)

    def to_dict(self):
        return {
            'u_id': self.u_id,
            'email': self.email,
            'password': self.password,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
            'permission_id': self.permission_id
        }


class Channel:
    def __init__(self, creator, name, is_public):
        self.channel_id = helpers.generate_id('channel_id')
        self.name = name
        self.is_public = is_public
        self.owner_members = [creator]
        self.all_members = [creator]
        self.messages = []
        self.standup = {
            'is_active': False,
            'starting_user': None,
            'time_finish': None,
            'messages': []
        }

    def add_owner(self, user):
        self.owner_members.append(user)

    def remove_owner(self, user):
        self.owner_members.remove(user)

    def add_member(self, user):
        self.all_members.append(user)

    def remove_member(self, user):
        self.all_members.remove(user)

    def is_member(self, user):
        return user in self.all_members

    @property
    def id_name(self):
        return {'channel_id': self.channel_id, 'name': self.name}

    @property
    def details(self):
        return {
            'name': self.name,
            'owner_members': [user.id_names for user in self.owner_members],
            'all_members': [user.id_names for user in self.all_members]
        }

    def is_owner(self, user):
        return user in self.owner_members

    def search(self, query_str):
        return [
            message for message in self.messages
            if query_str in message.message
        ]

    # def send_message(self, message_obj):
    #     self.messages.append(message_obj)

    # def get_message(self, message_id):
    #     for message in self.messages:
    #         if message_id == message.message_id:
    #             return message
    #     return None

    # def message_search(self, query_str):
    #     '''Retrieve all messages in a channel which contain the query string'''
    #     return [
    #         message.to_dict for message in self.messages
    #         if query_str in message.message
    #     ]

    def to_dict(self):
        messages = []
        for message in self.messages:
            messages.append(message.to_dict())
        return {
            'channel_id': self.channel_id,
            'name': self.name,
            'is_public': self.is_public,
            'owner_members': self.owner_members,
            'all_members': self.all_members,
            'messages': messages
        }


class Message:
    def __init__(self, sender, channel, message):
        self.message_id = helpers.generate_id('message_id')
        self.sender = sender
        self.channel = channel
        self.message = message
        self.time_created = helpers.utc_now()
        self.reacts = []
        self.is_pinned = False

    @property
    def u_id(self):
        return self.sender.u_id

    def details(self, user):
        message_reacts = []
        reacts = self.reacts
        for react in reacts:
            react_info = {
                'react_id': react.react_id,
                'u_ids': react.u_ids,
                'is_this_user_reacted': react in user.reacts
            }
            message_reacts.append(react_info)

        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': message_reacts,
            'is_pinned': self.is_pinned
        }

    def pin(self):
        self.is_pinned = True

    def unpin(self):
        self.is_pinned = False

    # def add_react(self, react_obj):
    #     self.reacts.append(react_obj)

    # def get_react(self, react_id):
    #     for react in self.reacts:
    #         if react_id == react.react_id:
    #             return react
    #     return None

    def to_dict(self):
        reacts = []
        for react in self.reacts:
            reacts.append(react.to_dict())
        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': reacts,
            'is_pinned': self.is_pinned
        }


class React:
    def __init__(self, react_id):
        self.react_id = react_id
        self.users = []

    def add_user(self, users):
        self.users.append(users)

    def remove_user(self, users):
        self.users.remove(users)

    @property
    def u_ids(self):
        return [user.u_id for user in self.users]

    def is_user_reacted(self, u_id):
        return u_id in self.u_ids

    def to_dict(self):
        return {'react_id': self.react_id, 'u_ids': self.u_ids}


class DataStore:
    def __init__(self):
        self.users = []
        self.channels = []
        self.messages = []
        self.token_blacklist = []
        self.permissions = {'owner': 1, 'member': 2}
        self.reactions = {'thumbs_up': 1}
        self.max_ids = {
            'u_id': 0,
            'channel_id': 0,
            'message_id': 0,
        }
        self.time_created = helpers.utc_now()

    def add_user(self, new_user):
        self.users.append(new_user)

    def add_channel(self, new_channel):
        self.channels.append(new_channel)

    def get_user(self, u_id=None, email=None):
        for user in self.users:
            if u_id == user.u_id or email == user.email:
                return user
        return None

    @property
    def u_ids(self):
        return [user.u_id for user in data_store.users]

    @property
    def users_all(self):
        return [user.profile for user in self.users]

    def get_channel(self, channel_id):
        for channel in self.channels:
            if channel_id == channel.channel_id:
                return channel
        return None

    def user_channels(self, u_id):
        '''Retrieve a list of a user's joined channels'''
        return [
            channel for channel in self.channels if u_id in channel.all_members
        ]

    @property
    def permission_values(self):
        return self.permissions.values()

    def is_admin(self, user):
        return user.permission_id == data_store.permissions['owner']

    def add_to_blacklist(self, token):
        self.token_blacklist.append(token)

    def generate_id(self, id_type):
        self.max_ids[id_type] += 1
        return self.max_ids[id_type]

    def to_dict(self):
        users = []
        for user in self.users:
            users.append(user.to_dict())
        channels = []
        for channel in self.channels:
            channels.append(channel.to_dict())

        return {
            'users': users,
            'channels': channels,
            'token_blacklist': self.token_blacklist,
            'permissions': self.permissions,
            'reactions': self.reactions,
            'max_ids': self.max_ids,
            'time_created': self.time_created
        }

    def reset(self):
        self.users.clear()
        self.channels.clear()
        self.messages.clear()
        self.token_blacklist.clear()

        for key in self.max_ids:
            self.max_ids[key] = 0

        self.time_created = int(datetime.utcnow().timestamp())


try:
    FILE = open('data_store.p', 'rb')
    data_store = pickle.load(FILE)
except FileNotFoundError:
    data_store = DataStore()


def save():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)


def autosave():
    timer = threading.Timer(1.0, autosave)
    timer.start()
    save()


if __name__ == "__main__":
    pass
