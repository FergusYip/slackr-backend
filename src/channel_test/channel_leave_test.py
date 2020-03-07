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
# testing channel_leave function.
# ===================================================================================


def test_leave(dummy_user1, dummy_user2, dummy_user3, channel1):
    '''
    Testing basic functionality of the channel_leave() function.
    '''

    # adding 2 users into the channel.
    channel.channel_join(dummy_user2['token'], channel1['channel_id'])
    channel.channel_join(dummy_user3['token'], channel1['channel_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 3

    # removing a user and checking if the size decremented.
    channel.channel_leave(dummy_user2['token'], channel1['channel_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 2


def test_leave_owner(dummy_user1, dummy_user2, channel1):
    '''
    Testing case when the only owner of a channel leaves.
    '''

    # adding a user to the channel.
    channel.channel_join(dummy_user2['token'], channel1['channel_id'])

    channel.channel_leave(dummy_user1['token'], channel1['channel_id'])

    details = channel.channel_details(
        dummy_user2['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 0

    assert len(details['all_members']) == 1


def test_leave_member(dummy_user1, channel1):
    '''
    Testing case when the only member of a channel leaves.
    '''

    channel.channel_leave(dummy_user1['token'], channel1['channel_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 0

    assert len(details['all_members']) == 0


def test_leave_uid(dummy_user1, dummy_user2, channel1):
    '''
    Testing case when the channel_leave() function is called by a 
    user that is not a member of the channel.
    '''

    with pytest.raises(AccessError):
        channel.channel_leave(dummy_user2['token'], channel1['channel_id'])


def test_leave_cid(dummy_user1):
    '''
    Testing case when an invalid channel_id is passed into the
    channel_leave() function.
    '''

    with pytest.raises(InputError):
        channel.channel_leave(dummy_user1['token'], -1)


def test_invalid_token_leave(channel1, invalid_token):
    '''
    Testing case when the token passed into the channel_leave() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_leave(invalid_token, channel1['channel_id'])
