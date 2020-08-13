import os
from dotenv import load_dotenv
load_dotenv()

PERMISSIONS = {'owner': 1, 'member': 2}
REACTIONS = {'thumbs_up': 1}
URL = os.environ['URL']
DATABASE_URL = os.environ['DATABASE_URL']
SECRET = os.environ['SECRET']
