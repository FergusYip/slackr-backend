from slackr import db
from slackr.models import user_react_identifier


class React(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    react_id = db.Column(db.Integer)
    users = db.relationship("User", secondary=user_react_identifier)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('message.message_id'),
                           nullable=False)

    def __init__(self, react_id):
        self.react_id = react_id

    def __repr__(self):
        return f'{self.message}: {self.react_id}'

    def details(self, user):
        ''' Details about the reaction from a given user's perspective.

        Parameters:
            user (obj): A user object.

        Return (dict):
            react_id (int): The ID of the reaction.
            u_ids (list):
                u_id (int): The u_id of a user who has reacted.
            is_this_user_reacted (bool): Whether the user has reacted or not.

        '''
        return {
            'react_id': self.react_id,
            'u_ids': [user.u_id for user in self.users],
            'is_this_user_reacted': self in user.reacts
        }
