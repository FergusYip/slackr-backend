import time
import threading
import pickle
from datetime import datetime

SECRET = 'the chunts'


class User:
    def __init__(self, u_id, email, password, name_first, name_last,
                 handle_str, permission_id):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle_str
        self.permission_id = permission_id

    def set_email(self, email):
        self.email = email

    def set_name(self, name_first, name_last):
        self.name_first = name_first
        self.name_last = name_last

    def set_handle(self, handle_str):
        self.handle_str = handle_str

    def change_permission(self, permission_id):
        self.permission_id = permission_id

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
    def __init__(self, creator_id, channel_id, name, is_public):
        self.channel_id = channel_id
        self.name = name
        self.is_public = is_public
        self.owner_members = [creator_id]
        self.all_members = [creator_id]
        self.messages = []

    def add_owner(self, u_id):
        self.owner_members.append(u_id)

    def remove_owner(self, u_id):
        self.owner_members.remove(u_id)

    def add_member(self, u_id):
        self.all_members.append(u_id)

    def remove_member(self, u_id):
        self.all_members.remove(u_id)

    def is_member(self, u_id):
        if u_id in self.all_members:
            return True
        return False

    def send_message(self, message_obj):
        self.messages.append(message_obj)

    def get_message(self, message_id):
        for message in self.messages:
            if message_id == message.message_id:
                return message
        return None

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
    def __init__(self, message_id, u_id, message):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = int(datetime.utcnow().timestamp())
        self.reacts = []
        self.is_pinned = False

    def add_react(self, react_obj):
        self.reacts.append(react_obj)

    def get_react(self, react_id):
        for react in self.reacts:
            if react_id == react.react_id:
                return react
        return None

    def pin(self):
        self.is_pinned = True

    def unpin(self):
        self.is_pinned = False

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
        self.u_ids = []

    def add_user(self, u_id):
        self.u_ids.append(u_id)

    def remove_user(self, u_id):
        self.u_ids.remove(u_id)

    def is_user_reacted(self, u_id):
        if u_id in self.u_ids:
            return True
        return False

    def to_dict(self):
        return {'react_id': self.react_id, 'u_ids': self.u_ids}


class DataStore:
    def __init__(self):
        self.users = []
        self.channels = []
        self.token_blacklist = []
        self.permissions = {'owner': 1, 'member': 2}
        self.reactions = {'thumbs_up': 1}
        self.max_ids = {
            'u_id': 0,
            'channel_id': 0,
            'message_id': 0,
        }
        self.time_created = int(datetime.utcnow().timestamp())

    def add_user(self, new_user):
        self.users.append(new_user)

    def add_channel(self, new_channel):
        self.channels.append(new_channel)

    def get_user(self, u_id=None, email=None):
        for user in self.users:
            if u_id == user.u_id or email == user.email:
                return user
        return None

    def get_all_u_id(self):
        return [user.u_id for user in data_store.users]

    def get_channel(self, channel_id):
        for channel in self.channels:
            if channel_id == channel.channel_id:
                return channel
        return None

    def get_permissions(self):
        return self.permissions.values()

    def is_owner(self, u_id):
        user = self.get_user(u_id=u_id)
        if user.permission_id == data_store.permissions['owner']:
            return True
        return False

    def add_to_blacklist(self, token):
        self.token_blacklist.append(token)

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
        self.token_blacklist.clear()

        self.max_ids['u_id'] = 0
        self.max_ids['channel_id'] = 0
        self.max_ids['message_id'] = 0

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
