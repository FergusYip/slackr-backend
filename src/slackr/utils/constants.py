import os
from dotenv import load_dotenv
load_dotenv()

PERMISSIONS = {'owner': 1, 'member': 2, 'bot': 3}
REACTIONS = {'thumbs_up': 1}
RESERVED_UID = {'hangman_bot': -95}
URL = os.environ['URL']
DATABASE_URL = os.environ['DATABASE_URL']
SECRET = os.environ['SECRET']
SECRET_KEY = os.environ['SECRET_KEY']
