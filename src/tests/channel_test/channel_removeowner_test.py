'''
System tests for channel removeowner function.
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
# testing channel_removeowner function.
# ===================================================================================


def test_removeowner(reset, dummy_user1, dummy_user2, dummy_user3, channel1):  # pylint: disable=W0621
    '''
    Testing the basic functionality of the channel_removeowner() function.
    '''

    # making dummy_user 2 and 3 members, and then owners of channel1.
    channel.channel_join(dummy_user2['token'], channel1['channel_id'])
    channel.channel_join(dummy_user3['token'], channel1['channel_id'])

    channel.channel_addowner(dummy_user1['token'], channel1['channel_id'],
                             dummy_user2['u_id'])

    channel.channel_addowner(dummy_user1['token'], channel1['channel_id'],
                             dummy_user3['u_id'])

    # checking if channel1 now has 3 owners.
    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['owner_members']) == 3

    # testing functionality of the channel_removeowner() function.
    channel.channel_removeowner(dummy_user1['token'], channel1['channel_id'],
                                dummy_user3['u_id'])

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['owner_members']) == 2

    # removeowner function should only make a user a non-owner. The total number of
    # users should still be the same.
    assert len(details['all_members']) == 3


def test_removeowner_uid(reset, dummy_user1, dummy_user3, channel1):  # pylint: disable=W0621
    '''
    Checking for AccessError when a user who is not an owner of a channel
    tries to remove another owner.
    '''

    channel.channel_join(dummy_user3['token'], channel1['channel_id'])

    with pytest.raises(AccessError):
        channel.channel_removeowner(dummy_user3['token'],
                                    channel1['channel_id'],
                                    dummy_user1['u_id'])

    details = channel.channel_details(dummy_user1['token'],
                                      channel1['channel_id'])

    assert len(details['owner_members']) == 1


def test_removeowner_empty(reset, dummy_user1, dummy_user2, channel2):  # pylint: disable=W0621
    '''
    Testing the channel_removeowner() function for a channel with no owners.
    '''

    channel.channel_invite(dummy_user2['token'], channel2['channel_id'],
                           dummy_user1['u_id'])

    channel.channel_removeowner(dummy_user2['token'], channel2['channel_id'],
                                dummy_user2['u_id'])

    details = channel.channel_details(dummy_user2['token'],
                                      channel2['channel_id'])

    assert len(details['owner_members']) == 0

    assert len(details['all_members']) == 2


def test_removeowner_cid(reset, dummy_user1, dummy_user2):  # pylint: disable=W0621
    '''
    Testing for InputError when an invalid channel id is passed into the
    channel_removeowner() function.
    '''

    with pytest.raises(InputError):
        channel.channel_removeowner(dummy_user1['token'], -1,
                                    dummy_user2['u_id'])


def test_removeowner_invalid_token(reset, dummy_user1, channel1,
                                   invalid_token):  # pylint: disable=W0621
    '''
    Testing case when the token passed into the channel_removeowner() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_removeowner(invalid_token, channel1['channel_id'],
                                    dummy_user1['u_id'])


def test_removeowner_insufficient_params(reset):
    '''Test input of invalid parameters into removeowner'''

    with pytest.raises(InputError):
        channel.channel_removeowner(None, None, None)
