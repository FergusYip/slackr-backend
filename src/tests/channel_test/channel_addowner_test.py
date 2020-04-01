'''
System tests for channel_addowner function.
'''

import pytest
import channel
from error import InputError
from error import AccessError


def test_addowner(reset, new_user, new_channel):
    '''
    Testing basic functionality of the channel_addowner() function.
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)
    channel.channel_join(member['token'], test_channel['channel_id'])

    channel.channel_addowner(owner['token'], test_channel['channel_id'],
                             member['u_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 2


def test_addowner_owner_self(reset, new_user, new_channel):
    '''
    Checking for InputError when dummy_user1, who is already an owner of channel1 tries
    to call the channel_addowner() function.
    '''
    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], test_channel['channel_id'],
                                 owner['u_id'])


def test_addowner_owner(reset, new_user, new_channel):
    '''
    Checking for AccessError when a user that is not an owner of the channel tries to
    call the channel_addowner() function.
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(AccessError):
        channel.channel_addowner(member['token'], test_channel['channel_id'],
                                 member['u_id'])


def test_addowner_cid(reset, new_user, new_channel):
    '''
    Checking for InputError when an invalid channel_id is passed into the
    channel_addowner() function.
    '''

    user = new_user(email='user@email.com')

    with pytest.raises(InputError):
        channel.channel_addowner(user['token'], -1, user['u_id'])


def test_addowner_invalid_u_id(reset, new_user, new_channel):
    '''
    Checking for InputError when an invalid user id is passed into the
    channel_addowner() function.
    '''

    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], test_channel['channel_id'],
                                 -1)


def test_addowner_not_member(reset, new_user, new_channel):
    '''
    Checking for InputError when the user id of a user who is not in
    the channel is passed into channel_addowner()
    '''

    owner = new_user(email='owner@email.com')
    stranger = new_user(email='stranger@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], test_channel['channel_id'],
                                 stranger['u_id'])


def test_addowner_invalid_token(reset, test_user, test_channel, invalid_token):
    '''
    Testing case when the token passed into the channel_addowner() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_addowner(invalid_token, test_channel['channel_id'],
                                 test_user['u_id'])


def test_addowner_insufficient_params(reset):
    '''Test input of invalid parameters into add_owner'''

    with pytest.raises(InputError):
        channel.channel_addowner(None, None, None)
