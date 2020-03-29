'''
System tests for channel join function.
'''

import pytest
import channel
from error import InputError
from error import AccessError


def test_join_new(reset, new_user, new_channel):
    '''
    Testing channel join for a public channel.
    '''

    owner = new_user(email='owner@email.com')
    stranger = new_user(email='stranger@email.com')
    test_channel = new_channel(owner)

    channel.channel_join(stranger['token'], test_channel['channel_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 2


def test_join_invalid_channel_id(reset, new_user):
    '''
    Testing channel join for an invalid channel id.
    '''

    user = new_user(email='user@email.com')

    with pytest.raises(InputError):
        channel.channel_join(user['token'], -1)


def test_join_private(reset, new_user, new_channel):
    '''
    Testing channel_join function for a private channel.
    '''

    user = new_user(email='user@email.com')
    stranger = new_user(email='stranger@email.com')
    test_channel = new_channel(user, is_public=False)

    with pytest.raises(AccessError):
        channel.channel_join(stranger['token'], test_channel['channel_id'])


def test_join_member(reset, new_user, new_channel):
    '''
    Testing channel_join function when the user is already a member of the channel.
    '''

    user = new_user(email='user@email.com')
    test_channel = new_channel(user)

    channel.channel_join(user['token'], test_channel['channel_id'])

    details = channel.channel_details(user['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 1


def test_join_invalid_token(reset, test_channel, invalid_token):
    '''
    Testing case when the token passed into the channel_join() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_join(invalid_token, test_channel['channel_id'])


def test_join_insufficient_params(reset):
    '''Test input of invalid parameters into join'''

    with pytest.raises(InputError):
        channel.channel_join(None, None)
