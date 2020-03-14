'''Python module to validate an Email courtesy of GeeksforGeeks'''

import re

# Make a regular expression for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def invalid_email(email):
    '''Check if an inputted email is invalid'''

    # pass the regualar expression and the email in search() method
    if (re.search(regex, email)):
        return False
    else:
        return True


if __name__ == '__main__':
    pass
