'''
System tests for channel join function.
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
def channel1(dummy_user1):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
    return c_id1


# Making another dummy channel (channel2) with valid details.
@pytest.fixture
def channel2(dummy_user2):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)
    return c_id2


# Making a private dummy channel (channel_priv) with valid details.
@pytest.fixture
def channel_priv(dummy_user3):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_priv = channels.channels_create(dummy_user3['token'], 'name3', False)
    return c_priv


# ===================================================================================
# testing channel_join function.
# ===================================================================================


def test_join_new(reset, dummy_user1, dummy_user3, channel1):  # pylint: disable=W0621
    '''
    Testing channel join for a public channel.
    '''

    channel.channel_join(dummy_user3['token'], channel1['channel_id'])

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['all_members']) == 2


def test_join_id(reset, dummy_user1):  # pylint: disable=W0621
    '''
    Testing channel join for an invalid channel id.
    '''

    with pytest.raises(InputError):
        channel.channel_join(dummy_user1['token'], -1)


def test_join_private(reset, dummy_user1, channel_priv):  # pylint: disable=W0621
    '''
    Testing channel_join function for a private channel.
    '''

    # channel_priv is made by dummy_user3. dummy_user1 should not be able to join.
    with pytest.raises(AccessError):
        channel.channel_join(dummy_user1['token'], channel_priv['channel_id'])


def test_join_member(reset, dummy_user1, channel1):  # pylint: disable=W0621
    '''
    Testing channel_join function when the user is already a member of the channel.
    '''

    channel.channel_join(dummy_user1['token'], channel1['channel_id'])

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['all_members']) == 1


def test_join_invalid_token(reset, channel1, invalid_token):  # pylint: disable=W0621
    '''
    Testing case when the token passed into the channel_join() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_join(invalid_token, channel1['channel_id'])
