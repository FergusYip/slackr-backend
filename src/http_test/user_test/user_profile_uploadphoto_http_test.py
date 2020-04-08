'''
Testing the functionality of the user_profile_uploadphoto function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# Using an image of UNSW ADFA in Canberra. It is 1200 x 943 pixels and 207KB in size.
img_url = 'http://www.unsw.adfa.edu.au/sites/default/files/uploads/ADFA%20Aerial.jpg'

# For invalid png image testing, will be using another UNSW image.
invalid_img = 'https://www.grandchallenges.unsw.edu.au/sites/default/files/2019-03/Grand%20Challenges%20slide.png'

# =====================================================
# ==== TESTING USER PROFILE UPLOADPHOTO FUNCTION ======
# =====================================================

def test_uploadphoto_return(reset, new_user):
    '''
    Testing the return type of the uploadphoto function.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': img_url,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200
    }

    return_type = requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).json()

    assert isinstance(return_type, dict)
    assert not return_type


def test_uploadphoto_avgcase(reset, new_user):
    '''
    Testing the average case scenario for when a user wants to select and crop an
    image to use.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': img_url,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200
    }

    # Will fail if an error is raised.
    requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_invalid_img_url(reset, new_user):
    '''
    Testing a case where the img_url is invalid.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': 'http://www.unsw.adfa.edu.au/notaworkinglink.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_invalid_x_start(reset, new_user):
    '''
    Testing a case where the x_start coordinate is invalid.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': img_url,
        'x_start': 1201,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_invalid_y_start(reset, new_user):
    '''
    Testing a case where the y_start coordinate is invalid.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': img_url,
        'x_start': 0,
        'y_start': 944,
        'x_end': 200,
        'y_end': 200
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_invalid_x_end(reset, new_user):
    '''
    Testing a case where the x_end coordinate is invalid.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': img_url,
        'x_start': 0,
        'y_start': 0,
        'x_end': 1201,
        'y_end': 200
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_invalid_y_end(reset, new_user):
    '''
    Testing a case where the y_end coordinate is invalid.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': img_url,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 944
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_notjpg(reset, new_user):
    '''
    Testing a case where the image is not a jpg, rather a png.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'img_url': invalid_img,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()


def test_uploadphoto_invalid_token(reset, new_user, invalid_token):
    '''
    Testing that an error is raised if an invalid token is used.
    '''

    user = new_user()

    func_input = {
        'token': invalid_token,
        'img_url': invalid_img,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/user/profile/uploadphoto', json=func_input).raise_for_status()
