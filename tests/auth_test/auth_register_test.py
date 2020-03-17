import json
import requests
import urllib
import pytest
# import auth
# import user
from error import AccessError, InputError

BASE_URL = 'http://127.0.0.1:8080'


def reset():
    requests.post(f"{BASE_URL}/workspace/reset")


def test_register_return_type(new_user):
    '''Test the types of values returned by auth_register'''
    reset()

    user = new_user()
    print(user)
    assert isinstance(user['u_id'], int)
    assert isinstance(user['token'], str)


# def test_register_duplicate():
#     '''Test the registration of multiple users with the same email'''
#     reset()

#     user_info = {
#         'email': 'theresavanaria@email.com',
#         'password': 'password',
#         'name_first': 'Theresa',
#         'name_last': 'Vanaria'
#     }

#     # # Setup 'existing' user
#     requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

# def test_register_password():
#     '''Test the input of various password lengths into auth_register'''
#     reset()

#     user_info = {
#         'email': 'theresavanaria@email.com',
#         'password': 'password',
#         'name_first': 'Theresa',
#         'name_last': 'Vanaria'
#     }

#     # Valid
#     requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     # <6 Password Length
#     user_info['password'] = '12345'
#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     # 32 character password that is within the (assumed) maximum length for password
#     user_info['password'] = 'i' * 32
#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

# def test_register_first_name():
#     '''Test the input of various first name lengths into auth_register'''
#     reset()

#     user_info = {
#         'email': 'theresavanaria@email.com',
#         'password': 'password',
#         'name_first': 'Theresa',
#         'name_last': 'Vanaria'
#     }

#     # Valid
#     requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     # <1 Character
#     user_info['name_first'] = ''
#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     # >50 Characters
#     user_info['name_first'] = 'i' * 51
#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

# def test_register_last_name():
#     '''Test the input of various last name lengths into auth_register'''
#     reset()

#     user_info = {
#         'email': 'theresavanaria@email.com',
#         'password': 'password',
#         'name_first': 'Theresa',
#         'name_last': 'Vanaria'
#     }

#     # Valid
#     requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     # <1 Character
#     user_info['name_last'] = ''
#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

#     # >50 Characters
#     user_info['name_last'] = 'i' * 51
#     with pytest.raises(InputError):
#         requests.post(f"{BASE_URL}/auth/register", json=user_info)

# def test_register_handle(test_user):
#     '''Test that the handle generated by auth_register matches assumption'''
#     reset()

#     query_string = urllib.parse.urlencode({
#         'token': test_user['token'],
#         'u_id': test_user['u_id']
#     })

#     user_profile = requests.get(f"{BASE_URL}/user/profile?{query_string}")
#     payload = user_profile.json()
#     assert payload['handle_str'] == 'firstlast'

# def test_register_unique_handle(new_user, get_user_profile):
#     '''Test that handles generated by auth_register are unique'''
#     reset()

#     user_1 = new_user('valid1@email.com')
#     user_profile_1 = get_user_profile(user_1['token'], user_1['u_id'])

#     user_2 = new_user('valid2@email.com')
#     user_profile_2 = get_user_profile(user_2['token'], user_2['u_id'])

#     assert user_profile_1['user']['handle_str'] != user_profile_2['user'][
#         'handle_str']

# def test_register_long_handle(new_user, get_user_profile):
#     '''Test that handles generated by auth_register are cut off at 20 characters'''
#     reset()

#     user = new_user('valid@email.com', 'password', '123456789testing',
#                     '123456789testing')
#     user_profile = get_user_profile(user['token'], user['u_id'])
#     assert user_profile['user']['handle_str'] == '123456789testing1234'

# def test_register_email_valid(valid_emails, new_user):
#     '''Test input of valid emails into auth_register'''
#     reset()

#     for email in valid_emails:
#         new_user(email)

# def test_register_email_invalid(invalid_emails, new_user):
#     '''Test input of invalid emails into auth_register'''
#     reset()

#     for email in invalid_emails:
#         with pytest.raises(InputError):
#             new_user(email)
