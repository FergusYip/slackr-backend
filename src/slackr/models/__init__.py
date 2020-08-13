from slackr import db

user_channel_identifier = db.Table(
    'user_channel_identifier',
    db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id')))

owner_channel_identifier = db.Table(
    'owner_channel_identifier',
    db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id')))

message_react_identifier = db.Table(
    'message_react_identifier',
    db.Column('message_id', db.Integer, db.ForeignKey('message.message_id')),
    db.Column('react_id', db.Integer, db.ForeignKey('react.react_id')))

user_react_identifier = db.Table(
    'user_react_identifier',
    db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
    db.Column('react_id', db.Integer, db.ForeignKey('react.react_id')))
