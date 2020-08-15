from slackr import db
from slackr.models.user import User
from slackr.utils.bot_loader import load_hangman_bot

db.create_all()

load_hangman_bot()