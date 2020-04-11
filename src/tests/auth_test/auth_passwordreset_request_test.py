''' System tests for auth_passwordreset_request'''
import time
import auth
from .read_email_helper import get_msg_from_chunts, delete_all_emails


def test_reset_request_sent_email(reset, new_user):  # pylint: disable=W0613
    '''Test that an email is sent to the user when a password reset is requested'''
    email = 'thechunts.slackr@gmail.com'
    new_user(email=email, password='pythonIsKool')
    delete_all_emails()
    auth.auth_passwordreset_request(email)
    time.sleep(10)
    assert len(get_msg_from_chunts()) == 1
    delete_all_emails()