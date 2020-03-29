'''
System tests for channel invite function.
'''

import pytest
import channel
from error import InputError
from error import AccessError


def test_invite_channel(reset, new_user, new_channel):
    '''
    Testing channel invite function with valid details
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)

    # testing channel invite function to valid channel.
    channel.channel_invite(owner['token'], test_channel['channel_id'],
                           member['u_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 2


def test_invalid_channel(reset, new_user, new_channel):
    '''
    Testing channel invite function with invalid channel id.
    '''

    user = new_user(email='user@email.com')

    # testing channel invite function to invalid channel.
    with pytest.raises(InputError):
        channel.channel_invite(user['token'], -1, user['u_id'])


def test_invalid_user(reset, new_user, new_channel):
    '''
    Testing channel invite function with invalid user.
    '''

    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    # testing channel invite for non-existent user.
    with pytest.raises(InputError):
        channel.channel_invite(owner['token'], test_channel['channel_id'], -1)

    # testing if there is only one member in channel1.
    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 1


def test_invite_access(reset, new_user, new_channel):
    '''
    Testing case when inviting user is not a member of a channel
    '''

    owner = new_user(email='owner@email.com')
    stranger = new_user(email='stranger@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(AccessError):
        channel.channel_invite(stranger['token'], test_channel['channel_id'],
                               stranger['u_id'])


def test_invite_invalid_token(reset, test_user, test_channel, invalid_token):
    '''
    Testing case when the token passed into the channel_invite() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_invite(invalid_token, test_channel['channel_id'],
                               test_user['u_id'])


def test_invite_insufficient_params(reset):
    '''Test input of invalid parameters into invite'''

    with pytest.raises(InputError):
        channel.channel_invite(None, None, None)