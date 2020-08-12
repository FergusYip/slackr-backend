'''Python module to validate an Email courtesy of GeeksforGeeks'''

import re


def invalid_email(email):
    '''Check if an inputted email is invalid'''

    # Make a regular expression for validating an Email
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    # pass the regualar expression and the email in search() method
    if re.search(regex, email):
        return False

    return True


if __name__ == '__main__':
    pass
