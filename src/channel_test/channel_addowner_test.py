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
# testing channel_addowner function.
# ===================================================================================


def test_addowner(dummy_user1, dummy_user3, channel1):
    '''
    Testing basic functionality of the channel_addowner() function.
    '''

    channel.channel_join(dummy_user3['token'], channel1['channel_id'])

    channel.channel_addowner(
        dummy_user1['token'], channel1['channel_id'], dummy_user3['u_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 2


def test_addowner_owner_self(dummy_user1, channel1):
    '''
    Checking for InputError when dummy_user1, who is already an owner of channel1 tries 
    to call the channel_addowner() function.
    '''

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user1['token'], channel1['channel_id'], dummy_user1['u_id'])


def test_addowner_owner(dummy_user1, dummy_user2, dummy_user3, channel1):
    '''
    Checking for AccessError when a user that is not an owner of the channel tries to
    call the channel_addowner() function.
    '''

    channel.channel_join(dummy_user3['token'], channel1['channel_id'])
    channel.channel_join(dummy_user2['token'], channel1['channel_id'])

    channel.channel_addowner(
        dummy_user2['token'], channel1['channel_id'], dummy_user3['u_id'])


def test_addowner_cid(dummy_user1, dummy_user2, channel1):
    '''
    Checking for InputError when an invalid channel_id is passed into the 
    channel_addowner() function.
    '''

    channel.channel_join(dummy_user2['token'], channel1['channel_id'])

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user1['token'], -1, dummy_user2['u_id'])


def test_addowner_uid(dummy_user2, dummy_user3, channel2):
    '''
    Checking for InputError when an invalid user id is passed into the 
    channel_addowner() function.
    Checking for InputError when the user id of a user who is not in 
    the channel is passed into channel_addowner()
    '''

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user2['token'], channel2['channel_id'], -1)

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user2['token'], channel2['channel_id'], dummy_user3['u_id'])


def test_invalid_token_addowner(dummy_user1, channel1, invalid_token):
    '''
    Testing case when the token passed into the channel_addowner() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_addowner(
            invalid_token, channel1['channel_id'], dummy_user1['u_id'])
