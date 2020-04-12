'''Pytest script for testing /auth/passwordreset/request'''
import time
import requests
from .read_email_helper import get_msg_from_chunts, delete_all_emails

BASE_URL = 'http://127.0.0.1:8080'


def test_reset_request_sent_email(reset, new_user):
    '''Test that an email is sent to the user when a password reset is requested'''
    email = 'thechunts.slackr@gmail.com'
    new_user(email=email, password='password')
    delete_all_emails()

    request_input = {'email': email}

    requests.post(f'{BASE_URL}/auth/passwordreset/request', json=request_input)

    time.sleep(10)
    assert len(get_msg_from_chunts()) == 1
    delete_all_emails()
