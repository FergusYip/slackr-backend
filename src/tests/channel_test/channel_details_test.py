'''
System tests for channel details function.
'''

import pytest
import channel
from error import InputError
from error import AccessError


def test_details_owner(reset, new_user, new_channel):
    '''
    Checking if channe1 owner is in owner_members.
    '''

    user = new_user(email='user@email.com')
    test_channel = new_channel(user)

    details = channel.channel_details(user['token'],
                                      test_channel['channel_id'])

    assert user['u_id'] in [user['u_id'] for user in details['owner_members']]


def test_details_added_owner(reset, new_user, new_channel):
    '''
    Test if details returns an updated number of channel owners
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)
    channel.channel_join(member['token'], test_channel['channel_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 1

    channel.channel_addowner(owner['token'], test_channel['channel_id'],
                             member['u_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 2


def test_details_all(reset, new_user, new_channel):
    '''
    Check if details contain correct number of members
    '''

    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 1

    member = new_user(email='member@email.com')
    channel.channel_join(member['token'], test_channel['channel_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 2


def test_details_invalid_channel_id(reset, new_user):
    '''
    Testing case when channel ID is invalid.
    '''

    user = new_user(email='user@email.com')

    with pytest.raises(InputError):
        channel.channel_details(user['token'], -1)


def test_details_not_member(reset, new_user, new_channel):
    '''
    Testing case when user asking for details isn't part of the channel.
    '''

    owner = new_user(email='owner@email.com')
    stranger = new_user(email='stranger@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(AccessError):
        channel.channel_details(stranger['token'], test_channel['channel_id'])


def test_details_invalid_token(reset, test_channel, invalid_token):
    '''
    Testing case when the token passed into the channel_details() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_details(invalid_token, test_channel['channel_id'])


def test_details_insufficient_params(reset):
    '''Test input of invalid parameters into details'''

    with pytest.raises(InputError):
        channel.channel_details(None, None)
