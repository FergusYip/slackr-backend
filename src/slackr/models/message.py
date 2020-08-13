from slackr import db, helpers


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    channel_id = db.Column(db.Integer,
                           db.ForeignKey('channel.channel_id'),
                           nullable=False)
    message = db.Column(db.String(1000))
    time_created = db.Column(
        db.Integer,
        nullable=False,
    )
    reacts = db.relationship("React", backref="message", lazy=True)
    is_pinned = db.Column(db.Boolean, default=False)
    is_hidden = db.Column(db.Boolean, default=False)

    def __init__(self, message, u_id, channel_id):
        self.message = message
        self.u_id = u_id
        self.channel_id = channel_id
        self.time_created = helpers.utc_now()

    def __repr__(self):
        return f'{self.time_created}: {self.message}'

    def details(self, user):
        ''' Get a dictionary of the message's information.

        Parameters:
            user (obj): An object of a user.

        Returns (dict):
            message_id (int): The message's unique identification number.
            u_id (int): The user who sent the message's u_id.
            message (str): The contents of the message to be sent.
            time_created (int): A unix timestamp of when the message was sent.
            reacts (list):
                react_id (int): The ID of the reaction denoting which type of reaction it is.
                u_ids (list):
                    u_id (int): The u_id of the users who have made this specific reaction.
                is_this_user_reacted (bool): Whether the user has reacted to the message.
            is_pinned (bool):  Whether the message has been pinned.

        '''
        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': [react.details(user) for react in self.reacts],
            'is_pinned': self.is_pinned
        }

    def get_react(self, react_id):
        ''' Return a react object attached to a message.

        Parameters:
            react_id (int): React ID as an integer.

        Returns:
            react (obj): A react object.

        '''
        for react in self.reacts:
            if react_id == react.react_id:
                return react
        return None
