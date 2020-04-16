''' Helper module with functions to access values from data_store'''
import string
import hashlib
import random
from datetime import datetime, timezone
import wikiquote


def utc_now():
    '''
    Returns the current UTC time in Unix time.

	Parameters:
		None

	Returns:
		(int) : Current UTC Time in Unix time
	'''

    return int(datetime.now(timezone.utc).timestamp())


def hash_pw(password):
    ''' Returns a hashed password

	Parameters:
		password (str): Password

	Returns:
		hashed password (str): Hashed password

	'''
    return hashlib.sha256(password.encode()).hexdigest()


def default_profile_img():
    ''' Return a link to a randomised default image'''
    colors = {
        'blue': 'https://i.imgur.com/HrDzaJo.jpg',
        'green': 'https://i.imgur.com/jETb01M.jpg',
        'purple': 'https://i.imgur.com/qmX0dIZ.jpg',
        'red': 'https://i.imgur.com/FTKy1XA.jpg'
    }
    return random.choice(list(colors.values()))


def get_word():
    '''
    Function to get a random word from wikiquote
    '''
    word = random.choice(wikiquote.random_titles(lang='en'))
    while not word.isalpha() and not check_ascii(word):
        word = random.choice(wikiquote.random_titles(lang='en'))
    return word.strip()


def check_ascii(word):
    '''
    Function to check if word is valid.
    '''
    for char in word:
        if char not in string.ascii_letters:
            return False

    return True


if __name__ == '__main__':
    pass
