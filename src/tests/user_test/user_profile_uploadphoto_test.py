'''
System tests for the user_profile_uploadphoto functionality.
'''

import pytest
import user
from error import AccessError, InputError

AREA_NORM = [0, 0, 200, 200]
AREA_HORIZONTAL_FLIP = [200, 0, 0, 200]
AREA_VERTICAL_FLIP = [0, 200, 200, 0]
AREA_HORI_VERTI_FLIP = [200, 200, 0, 0]

# Using an image of UNSW ADFA in Canberra. It is 1200 x 943 pixels and 207KB in size.
IMG_URL = 'http://www.unsw.adfa.edu.au/sites/default/files/uploads/ADFA%20Aerial.jpg'

# For invalid png image testing, will be using another UNSW image.
INVALID_IMG = 'https://www.grandchallenges.unsw.edu.au/sites/default/files/2019-03/Grand%20Challenges%20slide.png' #pylint: disable=C0301

# =====================================================
# ==== TESTING USER PROFILE UPLOADPHOTO FUNCTION ======
# =====================================================

def test_uploadphoto_return(reset, test_user):
    '''
    Testing the return type of the user_profile_uploadphoto function.
    '''

    return_type = user.user_profile_uploadphoto(test_user['token'], IMG_URL, AREA_NORM)
    assert isinstance(return_type, dict)
    assert not return_type


def test_uploadphoto_avgcase(reset, test_user):
    '''
    Testing an average case scenario of the uploadphoto function.
    '''

    user.user_profile_uploadphoto(test_user['token'], IMG_URL, AREA_NORM)


def test_uploadphoto_invalid_imgurl(reset, test_user):
    '''
    Testing that an InputError is raised if an invalid url is input.
    '''

    invalid_url = 'http://www.unsw.adfa.edu.au/notaworkinglink.jpg'
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], invalid_url, AREA_NORM)


def test_uploadphoto_invalid_xstart(reset, test_user):
    '''
    Testing that an invalid starting location for x will raise an error.
    '''

    invalid_area = [1201, 0, 200, 200]
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], IMG_URL, invalid_area)


def test_uploadphoto_invalid_ystart(reset, test_user):
    '''
    Testing that an invalid starting location for y will raise an error.
    '''

    invalid_area = [0, 944, 200, 200]
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], IMG_URL, invalid_area)


def test_uploadphoto_invalid_xend(reset, test_user):
    '''
    Testing that an invalid ending location for x will raise an error.
    '''

    invalid_area = [0, 0, 1201, 200]
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], IMG_URL, invalid_area)


def test_uploadphoto_invalid_yend(reset, test_user):
    '''
    Testing that an invalid ending location for y will raise an error.
    '''

    invalid_area = [0, 0, 200, 944]
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], IMG_URL, invalid_area)


def test_uploadphoto_notjpg(reset, test_user):
    '''
    Testing that an image url that is not a .jpg file will raise an error.
    '''

    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], INVALID_IMG, AREA_NORM)


def test_uploadphoto_greater_xend(reset, test_user):
    '''
    Testing the average case scenario for if a user inputs a greater x_start location than x_end.
    This will flip the image horizontally.
    '''

    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], IMG_URL, AREA_HORIZONTAL_FLIP)


def test_uploadphoto_greater_yend(reset, test_user):
    '''
    Testing the average case scenario for if a user inputs a greater y_start location than y_end.
    This will flip the image vertically.
    '''

    with pytest.raises(InputError):
        user.user_profile_uploadphoto(test_user['token'], IMG_URL, AREA_VERTICAL_FLIP)


def test_uploadphoto_invalid_token(reset, invalid_token):
    '''
    Testing that using the uploadphoto function with an invalid token will raise an
    AccessError.
    '''

    with pytest.raises(AccessError):
        user.user_profile_uploadphoto(invalid_token, IMG_URL, AREA_NORM)
