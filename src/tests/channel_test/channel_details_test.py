'''
System tests for channel details function.
'''

import pytest
import channel
import channels
import auth
from error import InputError
from error import AccessError

# ================================= MAKING USERS ====================================


# Making a dummy user (dummy_user1) with valid details.
@pytest.fixture
def dummy_user1():
    '''
    Pytest fixture for a dummy user for testing.
    '''

    dummy_user1 = auth.auth_register('something.else@domain.com',
                                     'GreatPassword04', 'something', 'else')
    return dummy_user1


# Making another dummy user (dummy_user2) with valid details.
@pytest.fixture
def dummy_user2():
    '''
    Pytest fixture for a dummy user for testing.
    '''

    dummy_user2 = auth.auth_register('dummy.user@domain.com',
                                     'BetterPassword09', 'dummy', 'user')
    return dummy_user2


# Making another dummy user (dummy_user3) with valid details.
@pytest.fixture
def dummy_user3():
    '''
    Pytest fixture for a dummy user for testing.
    '''

    dummy_user3 = auth.auth_register('dummy.user3@domain.com',
                                     'ReallCoolPassword9800!', 'dummy',
                                     'three')
    return dummy_user3


# ================================= MAKING CHANNELS ====================================


# Making a dummy channel (channel1) with valid details.
@pytest.fixture
def channel1(reset, dummy_user1):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
    return c_id1


# Making another dummy channel (channel2) with valid details.
@pytest.fixture
def channel2(reset, dummy_user2):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)
    return c_id2


# Making a private dummy channel (channel_priv) with valid details.
@pytest.fixture
def channel_priv(reset, dummy_user3):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_priv = channels.channels_create(dummy_user3['token'], 'name3', False)
    return c_priv


# ===================================================================================
# testing channel_details function.
# ===================================================================================


def test_details_owner(reset, dummy_user1, channel1):  # pylint: disable=W0621
    '''
    Checking if channe1 has dummy_user1 in owner_members.
    '''

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert dummy_user1['u_id'] in [
        user['u_id'] for user in details['owner_members']
    ]


def test_details_added_owner(reset, dummy_user1, dummy_user2, channel1):  # pylint: disable=W0621
    '''
    Adding another owner (dummy_user2) to name1 and checking if the channel
    has 2 owners.
    '''

    channel.channel_join(dummy_user2['token'], channel1['channel_id'])

    channel.channel_addowner(dummy_user1['token'], channel1['channel_id'],
                             dummy_user2['u_id'])

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['owner_members']) == 2


def test_details_all(reset, dummy_user1, channel1):  # pylint: disable=W0621
    '''
    Checking if channel1 has 1 user in all_members.
    '''

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['all_members']) == 1


def test_details_invalid(reset, dummy_user1, channel2):  # pylint: disable=W0621
    '''
    Testing case when channel ID is invalid.
    Testing case when user asking for details isn't part of the channel.
    '''

    with pytest.raises(InputError):
        channel.channel_details(dummy_user1['token'], -1)

    # Testing case when the user asking for details isn't part of the channel.
    with pytest.raises(AccessError):
        channel.channel_details(dummy_user1['token'], channel2['channel_id'])


def test_details_invalid_token(reset, channel1, invalid_token):  # pylint: disable=W0621
    '''
    Testing case when the token passed into the channel_details() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_details(invalid_token, channel1['channel_id'])
