''' System tests for channels_create'''
import pytest
import channel
import channels
from error import InputError, AccessError


def test_create_public(reset, test_user):  # pylint: disable=W0613
    '''Test that any users can join a public channel'''

    test_channel = channels.channels_create(test_user['token'], 'Channel',
                                            True)
    channel.channel_join(test_user['token'], test_channel['channel_id'])
    details = channel.channel_details(test_user['token'],
                                      test_channel['channel_id'])
    assert test_user['u_id'] == details['all_members'][0]['u_id']


def test_create_private(reset, new_user):  # pylint: disable=W0613
    '''Test that an unauthorised user cannot join a private channel'''

    owner = new_user(email='owner@slackr.com')
    stranger = new_user(email='stranger@danger.com')

    test_channel = channels.channels_create(owner['token'], 'Channel', False)

    with pytest.raises(AccessError):
        channel.channel_join(stranger['token'], test_channel['channel_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])
    assert len(details['all_members']) == 1


def test_create_types(reset, test_user):  # pylint: disable=W0613
    '''Test the types returned by channels_user'''

    new_channel = channels.channels_create(test_user['token'], 'Channel', True)
    assert isinstance(new_channel, dict)
    assert isinstance(new_channel['channel_id'], int)


def test_create_long_name(reset, test_user):  # pylint: disable=W0613
    '''Test creation of channel with name length > 20'''

    with pytest.raises(InputError):
        channels.channels_create(test_user['token'], 'i' * 21, True)


def test_create_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that channels_create raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_create(invalid_token, 'Channel', True)


def test_create_invalid_params(reset):  # pylint: disable=W0613
    '''Test input of invalid parameters into channels_create'''

    with pytest.raises(InputError):
        channels.channels_create(None, None, None)
