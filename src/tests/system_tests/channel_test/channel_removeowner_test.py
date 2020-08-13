'''
System tests for channel removeowner function.
'''

import pytest
import channel
from error import InputError
from error import AccessError


def test_removeowner(reset, new_user, new_channel):
    '''
    Testing the basic functionality of the channel_removeowner() function.
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)

    channel.channel_join(member['token'], test_channel['channel_id'])

    channel.channel_addowner(owner['token'], test_channel['channel_id'],
                             member['u_id'])

    # checking if channel1 now has 2 owners.
    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 2

    # testing functionality of the channel_removeowner() function.
    channel.channel_removeowner(owner['token'], test_channel['channel_id'],
                                member['u_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 1
    assert len(details['all_members']) == 2


def test_removeowner_not_owner(reset, new_user, new_channel):
    '''
    Checking for AccessError when a user who is not an owner of a channel
    tries to remove another owner.
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)

    channel.channel_join(member['token'], test_channel['channel_id'])

    with pytest.raises(AccessError):
        channel.channel_removeowner(member['token'],
                                    test_channel['channel_id'], owner['u_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert len(details['owner_members']) == 1


def test_removeowner_only_owner(reset, new_user, new_channel):
    '''
    Testing the channel_removeowner() function to remove only owner
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)

    channel.channel_join(member['token'], test_channel['channel_id'])

    channel.channel_removeowner(owner['token'], test_channel['channel_id'],
                                owner['u_id'])

    details = channel.channel_details(owner['token'],
                                      test_channel['channel_id'])

    assert not details['owner_members']

    assert len(details['all_members']) == 2


def test_removeowner_invalid_channel_id(reset, test_user):
    '''
    Testing for InputError when an invalid channel id is passed into the
    channel_removeowner() function.
    '''

    with pytest.raises(InputError):
        channel.channel_removeowner(test_user['token'], -1, test_user['u_id'])


def test_removeowner_invalid_token(reset, test_user, test_channel,
                                   invalid_token):
    '''
    Testing case when the token passed into the channel_removeowner() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_removeowner(invalid_token, test_channel['channel_id'],
                                    test_user['u_id'])


def test_removeowner_not_member(reset, new_user, new_channel):
    '''
    Test that a error is raised when the authorised user is not a member
    '''

    owner = new_user(email='owner@email.com')
    member = new_user(email='member@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(InputError):
        channel.channel_removeowner(owner['token'], test_channel['channel_id'],
                                    member['u_id'])


def test_removeowner_invalid_u_id(reset, new_user, new_channel):
    '''
    Test that a error is raised when the authorised user is not a owner
    '''

    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    with pytest.raises(InputError):
        channel.channel_removeowner(owner['token'], test_channel['channel_id'],
                                    -1)


def test_removeowner_insufficient_params(reset):
    '''Test input of invalid parameters into removeowner'''

    with pytest.raises(InputError):
        channel.channel_removeowner(None, None, None)
