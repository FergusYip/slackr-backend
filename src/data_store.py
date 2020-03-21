from datetime import datetime, timezone

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


class Message:
    def __init__(self, message_id, u_id, message):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = int(datetime.now(timezone.utc).timestamp())
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


class DataStore:
    def __init__(self):
        self.users = []
        self.channels = []
        self.token_blacklist = []
        self.permissions = {'owner': 1, 'member': 2}
        self.reactions = {'thumbs_up': 1}

    def add_user(self, new_user):
        self.users.append(new_user)

    def add_channel(self, new_channel):
        self.channels.append(new_channel)

    def get_user(self, u_id):
        for user in self.users:
            if u_id == user.u_id:
                return user
        return None

    def get_channel(self, channel_id):
        for channel in self.channels:
            if channel_id == channel.channel_id:
                return channel
        return None

    def reset(self):
        self.users.clear()
        self.channels.clear()
        self.token_blacklist.clear()


'''
Sample Data Store Structure

data_store = {
    'users': [{
            'u_id': u_id,
            'email': email,
            'password': hash_pw(password),
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': generate_handle(name_first, name_last),
            'permission_id': permission_id
        }],
    'channels': [{
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [u_id],
        'all_members': [u_id],
        'messages': [{
            'message_id': message_id,
            'u_id': u_id,
            'message': message,
            'time_created': time_created,
            'reacts': [{
                'react_id': react_id,
                'u_ids': [u_id],
            }],
            'is_pinned': is_pinned
        }]
    }],
    'tokens': [],
    'permissions': {
        'owner': 1,
        'member': 2
    }
}

'''

if __name__ == "__main__":
    pass
