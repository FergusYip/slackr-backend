from datetime import datetime
from slackr import db
from slackr import helpers
from slackr.utils.constants import PERMISSIONS


class Standup:
    ''' Standup Object '''
    def __init__(self):
        self._is_active = False
        self._starting_user = None
        self._time_finish = None
        self._messages = []

    @property
    def is_active(self):
        ''' Whether the standup is active (bool) '''
        return self._is_active

    @property
    def starting_user(self):
        ''' The user who started the standup (user_obj) '''
        return self._starting_user

    @property
    def time_finish(self):
        ''' Standup end time (int) '''
        return self._time_finish

    @property
    def messages(self):
        ''' Standup messages (list[message_obj]) '''
        return self._messages

    def start(self, user, time_finish):
        ''' Start the standup

        Parameters:
            user (obj): The user who started the standup
            time_finished (int): The desired end time of the standup

        '''
        self._is_active = True
        self._starting_user = user
        self._time_finish = time_finish

    def stop(self):
        ''' Stop the standup

        Parameters:
            user (obj): The user who started the standup
            time_finished (int): The desired end time of the standup

        Return:
            joined_message (str): Standup summary message (joined string of all
                                  standup messages)

        '''
        joined_message = ''
        for message in self._messages:
            joined_message += f"{message['handle_str']}: {message['message']}\n"

        self._is_active = False
        self._starting_user = None
        self._time_finish = None
        self._messages.clear()

        return joined_message

    def send(self, user, message):
        ''' Send a standup message

        Parameters:
            user (obj): The user who sent the message
            message (str): Message

        '''
        message_dict = {'handle_str': user.handle_str, 'message': message}
        self.messages.append(message_dict)


db.create_all()