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
# testing channel_invite function.
# ===================================================================================


def test_invite_channel(dummy_user1, dummy_user2, channel1):
    '''
    Testing channel invite function with valid and invalid channel details.
    Inviting dummy_user2 to channel1, and attempting to invite dummy_user2 
    to a channel with invalid channel_id.
    '''

    # testing channel invite function to valid channel.
    channel.channel_invite(
        dummy_user1['token'], channel1['channel_id'], dummy_user2['u_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 2

    # testing channel invite function to invalid channel.
    with pytest.raises(InputError):
        channel.channel_invite(
            dummy_user1['token'], -1, dummy_user2['u_id'])


def test_invite_user(dummy_user1, dummy_user2, channel1):
    '''
    Testing channel invite function for a non-existent user.
    Checking if dummy_user2 is in channel1 using a loop.
    '''

    # testing channel invite for non-existent user.
    with pytest.raises(InputError):
        channel.channel_invite(
            dummy_user1['token'], channel1['channel_id'], 69)

    # testing if there is only one member in channel1.
    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 1


def test_invite_access(dummy_user1, dummy_user2, channel2):
    '''
    Testing case when inviting user is not a member of a channel.channel_
    At this point - the channel name1 has both users (dummy_user1 and dummy_user2)
    but the channel name2 only has dummy_user2.
    '''
    with pytest.raises(AccessError):
        channel.channel_invite(
            dummy_user1['token'], channel2, dummy_user2['u_id'])


def test_invite_invalid_token(dummy_user1, channel1, invalid_token):
    '''
    Testing case when the token passed into the channel_invite() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_invite(
            invalid_token, channel1['channel_id'], dummy_user1['u_id'])