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
# testing channel_details function.
# ===================================================================================


def test_details_owner(dummy_user1, channel1):
    '''
    Checking if channe1 has dummy_user1 in owner_members.
    '''

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    owner = False

    # for user in details['owner_members']:
    #     if user['u_id'] == dummy_user1['u_id']:
    if dummy_user1['u_id'] in details['owner_members']:
        owner = True

    assert owner is True


def test_details_added_owner(dummy_user1, dummy_user2, channel1):
    '''
    Adding another owner (dummy_user2) to name1 and checking if the channel
    has 2 owners.
    '''

    channel.channel_addowner(
        dummy_user1['token'], channel1['channel_id'], dummy_user2['u_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 2


def test_details_all(dummy_user1, channel1):
    '''
    Checking if channel1 has 1 user in all_members.
    '''

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 1


def test_details_invalid(dummy_user1, channel2):
    '''
    Testing case when channel ID is invalid.
    Testing case when user asking for details isn't part of the channel.
    '''

    with pytest.raises(InputError):
        channel.channel_details(dummy_user1['token'], -1)

    # Testing case when the user asking for details isn't part of the channel.
    with pytest.raises(AccessError):
        channel.channel_details(dummy_user1['token'], channel2['channel_id'])


def test_details_invalid_token(channel1, invalid_token):
    '''
    Testing case when the token passed into the channel_details() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_details(invalid_token, channel1['channel_id'])
