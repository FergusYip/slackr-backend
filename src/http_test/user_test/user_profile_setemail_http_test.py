'''
Testing the functionality of the user_profile_setemail function.

Parameters used:
    reset: Reset is a function defined in conftest.py that restores all values
           in the data_store back to being empty.
    new_user: A function defined in conftest.py that will create a new user based on
              default values that can be specified. Returns the u_id and token.
    invalid_emails: A fixture in conftest.py that returns a tuple of invalid emails for test
                    purposes.
    valid_emails: A fixture in conftest.py that returns a tuple of valid emails.
    invalid_token: A function defined in conftest.py that creates a new user, stores the
                   token, and logs the user out. It will then return this invalid token.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_profile_setemail_return(reset, new_user):
    '''
    Testing the return types of the user_profile_setemail function.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'email': 'test@test.com'
    }

    set_email = requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).json()

    assert isinstance(set_email, dict)


def test_setemail(reset, new_user):
    '''
    Testing the functionality of updating the user's email.
    '''

    # ================ SET-UP ===================

    user = new_user(email='tester@test.com')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_email = 'tester@test.com'

    assert user_pre_info['email'] == expected_email

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'email': 'newtest@test.com'
    }

    requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).json()

    user_post_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_email = 'newtest@test.com'

    assert user_post_info['email'] == expected_email


def test_changetocurrent(reset, new_user):
    '''
    Testing that changing the email to the user's current email will
    return an empty dictionary and not raise an error.
    '''

    # ================ SET-UP ===================

    user = new_user(email='test@test.com')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_email = 'test@test.com'

    assert user_pre_info['email'] == expected_email

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'email': 'test@test.com'
    }

    set_email = requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).json()

    assert isinstance(set_email, dict)


def test_invalid_emails(reset, new_user, invalid_emails):
    '''
    Testing that trying to change the email to one of which is invalid will
    raise an error.
    '''

    user = new_user(email='test@test.com')

    for email in invalid_emails:
        func_input = {
            'token': user['token'],
            'email': email
        }
        with pytest.raises(requests.HTTPError):
            requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).raise_for_status()

def test_valid_emails(reset, new_user, valid_emails):
    '''
    Testing that trying to change the email to one of which is valid will
    not raise an error.
    '''

    user = new_user(email='test@test.com')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    for email in valid_emails:
        func_input = {
            'token': user['token'],
            'email': email
        }
        requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).raise_for_status()
        user_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()

        assert email == user_info['email']

def test_email_used(reset, new_user):
    '''
    Testing that trying to change the email to one that is already being
    used by another user will raise an error.
    '''

    # ================ SET-UP ===================

    user = new_user(email='test@test.com')
    second_user = new_user(email='notused@test.com')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_email = 'test@test.com'

    # Assert that string expected_email is being used.
    assert user_info['email'] == expected_email

    # ================ TESTING ==================

    func_input = {
        'token': second_user['token'],
        'email': expected_email
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).raise_for_status()


def test_invalid_token(reset, invalid_token):
    '''
    Testing that an invalid token will raise an error.
    '''

    func_input = {
        'token': invalid_token,
        'email': 'tester@test.com'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/setemail', json=func_input).raise_for_status()
