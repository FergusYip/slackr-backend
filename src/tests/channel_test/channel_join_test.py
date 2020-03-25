import channel
import channels
import pytest
import auth
import message
from error import InputError
from error import AccessError

# ================================= MAKING USERS ====================================

# Making a dummy user (dummy_user1) with valid details.
@pytest.fixture
def dummy_user1():
    dummy_user1 = auth.auth_register(
        'something.else@domain.com', 'GreatPassword04', 'something', 'else')
    return dummy_user1


# Making another dummy user (dummy_user2) with valid details.
@pytest.fixture
def dummy_user2():
    dummy_user2 = auth.auth_register(
        'dummy.user@domain.com', 'BetterPassword09', 'dummy', 'user')
    return dummy_user2

# Making another dummy user (dummy_user3) with valid details.
@pytest.fixture
def dummy_user3():
    dummy_user3 = auth.auth_register(
        'dummy.user3@domain.com', 'ReallCoolPassword9800!', 'dummy', 'three')
    return dummy_user3


# ================================= MAKING CHANNELS ====================================


# Making a dummy channel (channel1) with valid details.
@pytest.fixture
def channel1(dummy_user1):
    c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
    return c_id1


# Making another dummy channel (channel2) with valid details.
@pytest.fixture
def channel2(dummy_user2):
    c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)
    return c_id2


# Making a private dummy channel (channel_priv) with valid details.
@pytest.fixture
def channel_priv(dummy_user3):
    c_priv = channels.channels_create(dummy_user3['token'], 'name3', False)
    return c_priv


# ===================================================================================
# testing channel_join function.
# ===================================================================================


def test_join_new(dummy_user1, dummy_user3, channel1):
    '''
    Testing basic functions of channel_join.
    New user joining channel1 (public) and checking if channel1 has 3 members.
    '''

    channel.channel_join(dummy_user3['token'], channel1['channel_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 2


def test_join_id(dummy_user1):
    '''
    Testing for an InputError when an invalid channel id is passed into the 
    channel_join() function.
    '''

    with pytest.raises(InputError):
        channel.channel_join(dummy_user1['token'], -1)


def test_join_private(dummy_user1, channel_priv):
    '''
    Testing channel_join function for a private channel.
    '''

    with pytest.raises(AccessError):
        channel.channel_join(dummy_user1['token'], channel_priv['channel_id'])


def test_join_member(dummy_user1, channel1):
    '''
    Testing channel_join function when the user is already a member of the channel.
    '''

    channel.channel_join(dummy_user1['token'], channel1['channel_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 1


def test_join_invalid_token(channel1, invalid_token):
    '''
    Testing case when the token passed into the channel_join() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_join(invalid_token, channel1['channel_id'])
