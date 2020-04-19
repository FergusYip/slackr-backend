''' System tests for channels_list'''
import pytest
import channels
from error import AccessError, InputError


def test_list(reset, new_user):  # pylint: disable=W0613
    '''Test that channels_list only returns channels the user is in'''

    user_1 = new_user(email='user_1@email.com')
    user_2 = new_user(email='user_2@email.com')

    user_1_channel = channels.channels_create(user_1['token'], 'User 1', True)
    user_2_channel = channels.channels_create(user_2['token'], 'User 2', True)

    joined_channels = channels.channels_list(user_1['token'])['channels']
    assert len(joined_channels) == 1

    assert user_1_channel['channel_id'] in [
        channel['channel_id'] for channel in joined_channels
    ]
    assert user_2_channel['channel_id'] not in joined_channels


def test_list_return_type(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test that the types of the values returned are correct'''
    new_channel(test_user, 'Channel')
    all_channels = channels.channels_list(test_user['token'])['channels']
    assert isinstance(all_channels, list)
    assert isinstance(all_channels[0], dict)
    assert isinstance(all_channels[0]['channel_id'], int)
    assert isinstance(all_channels[0]['name'], str)


def test_list_no_channels(reset, test_user):  # pylint: disable=W0613
    '''Test that channels_list doesn't return any channels when there aren't any'''

    all_channels = channels.channels_list(test_user['token'])['channels']
    assert not all_channels


def test_list_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that channels_list raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_list(invalid_token)


def test_list_invalid_params(reset):  # pylint: disable=W0613
    '''Test input of invalid parameters into channels_list'''

    with pytest.raises(InputError):
        channels.channels_list(None)
