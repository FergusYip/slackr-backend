from slackr.models.user import User
from slackr.utils.constants import RESERVED_UID, PERMISSIONS
from slackr import db


def load_hangman_bot():
    bot = User.query.get(RESERVED_UID['hangman_bot'])
    if not bot:
        bot = User('', '', 'Hangman Bot', '', 'hangman_bot')
        bot.u_id = RESERVED_UID['hangman_bot']
        bot.permission_id = PERMISSIONS['bot']
        db.session.add(bot)
        db.session.commit()