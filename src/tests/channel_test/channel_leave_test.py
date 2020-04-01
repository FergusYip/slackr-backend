'''
System tests for channel leave function.
'''

import pytest
import channel
from error import InputError
from error import AccessError


def test_leave(reset, new_user, new_channel):
    '''
    Testing channel leave for a public channel.
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')

    test_channel = new_channel(owner)

    channel.channel_join(member['token'], test_channel['channel_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 2

    # removing a user and checking if the size decremented.
    channel.channel_leave(member['token'], test_channel['channel_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['all_members']) == 1


def test_leave_owner(reset, new_user, new_channel):
    '''
    Testing case when the only owner of a channel leaves.
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')

    test_channel = new_channel(owner)

    # adding a user to the channel.
    channel.channel_join(member['token'], test_channel['channel_id'])

    channel.channel_leave(owner['token'], test_channel['channel_id'])

    details = channel.channel_details(member['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 0

    assert len(details['all_members']) == 1


def test_leave_user(reset, new_user, test_channel):
    '''
    Testing channel leave when non-member leaves.
    '''

    user = new_user()

    with pytest.raises(AccessError):
        channel.channel_leave(user['token'], test_channel['channel_id'])


def test_leave_invalid_channel_id(reset, test_user):
    '''
    Testing case when an invalid channel_id is passed into the
    channel_leave() function.
    '''

    with pytest.raises(InputError):
        channel.channel_leave(test_user['token'], -1)


def test_leave_invalid_token(reset, test_channel, invalid_token):
    '''
    Testing case when the token passed into the channel_leave() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_leave(invalid_token, test_channel['channel_id'])


def test_leave_insufficient_params(reset):
    '''Test input of invalid parameters into leave'''

    with pytest.raises(InputError):
        channel.channel_leave(None, None)
