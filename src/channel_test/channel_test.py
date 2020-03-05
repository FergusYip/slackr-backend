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

    # testing channel invite function to invalid channel.
    with pytest.raises(InputError):
        channel.channel_invite(
            dummy_user1['token'], '3555', dummy_user2['u_id'])


def test_invite_user(dummy_user1, dummy_user2, channel1):
    '''
    Testing channel invite function for a non-existent user.
    Checking if dummy_user2 is in channel1 using a loop.
    '''

    # testing channel invite for non-existent user.
    with pytest.raises(InputError):
        channel.channel_invite(
            dummy_user1['token'], channel1['channel_id'], 69)

    # testing if the user with user id dummy_user2[u_id] exists in channel c_id1.
    # this should pass if line 19 executed.
    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])
    user_in_channel = False

    for user in details['all_members']:
        if user['u_id'] == dummy_user2['u_id']:
            user_in_channel = True

    assert user_in_channel == True


def test_invite_access(dummy_user1, dummy_user2, channel2):
    '''
    Testing case when inviting user is not a member of a channel.channel_
    At this point - the channel name1 has both users (dummy_user1 and dummy_user2)
    but the channel name2 only has dummy_user2.
    '''
    with pytest.raises(AccessError):
        channel.channel_invite(
            dummy_user1['token'], channel2, dummy_user2['u_id'])


# ===================================================================================
# testing channel_details function.
# ===================================================================================


def test_details_owner(dummy_user1, channel1):
    '''
    Checking if channel name1 has dummy_user1 in owner_members.
    '''

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])
    owner = False

    for user in details['owner_members']:
        if user['u_id'] == dummy_user1['u_id']:
            owner = True

    assert owner == True


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
    Checking if channel name1 has 2 users in all_members.
    '''

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['all_members']) == 2


def test_details_invalid(dummy_user1, channel2):
    '''
    Testing case when channel ID is invalid.
    Testing case when user asking for details isn't part of the channel.
    '''

    with pytest.raises(InputError):
        channel.channel_details(dummy_user1['token'], 42045)

    # Testing case when user asking for details isn't part of the channel
    # at this point, channel name2 has only dummy_user2 as members.
    # testing case when dummy_user1 asks for details about channel name2.
    with pytest.raises(AccessError):
        channel.channel_details(dummy_user1['token'], channel2['channel_id'])


# ===================================================================================
# testing channel_messages function.
# ===================================================================================

def test_messages_sent(dummy_user1, dummy_user2, channel1):
    '''
    dummy_user1 sends a message into channel1 and then dummy_user2 sends a reply.
    assert that the length of the message history is now 2.
    assert that the start value is actually 0.
    '''

    message.message_send(
        dummy_user1['token'], channel1['channel_id'], "Im Batman")

    message.message_send(
        dummy_user2['token'], channel1['channel_id'], "yeah right")

    # Getting the history of messages from 0 to 50 (by default) and checking if the length of the history is 2.
    history = channel.channel_messages(
        dummy_user1['token'], channel1['channel_id'], 0)

    assert len(history['messages']) == 2

    assert(history['start'] == 0)


def test_messages_remove(dummy_user2, channel1):
    '''
    dummy_user2 sends another message, then removes it. 
    assert that the length of the message history is still 2.
    '''

    message_id = message.message_send(
        dummy_user2['token'], channel1['channel_id'], "idk why I talk to you.")

    message.message_remove(dummy_user2['token'], message_id['message_id'])

    history = channel.channel_messages(
        dummy_user2['token'], channel1['channel_id'], 0)

    assert len(history['messages']) == 2


def test_messages_id(dummy_user1):
    '''
    Checking for an InputError when an invalid channel_id is passed into the 
    channel_messages function.
    '''

    with pytest.raises(InputError):
        channel.channel_messages(dummy_user1['token'], 31415926, 0)


def test_messages_start(dummy_user1, channel1):
    '''
    Checking for an InputError when the channel_messages function get a start
    that is greater than the size of the message history
    '''

    history = channel.channel_messages(
        dummy_user1['token'], channel1['channel_id'], 0)

    with pytest.raises(InputError):
        channel.channel_messages(
            dummy_user1['token'], channel1['channel_id'], len(history['messages']) + 1)


def test_messages_access(dummy_user1, channel2):
    '''
    Checking for an AccessError when dummy_user1 asks for message history of 
    channel2.
    Because at this point channel2 only has user2 as a member.
    '''

    with pytest.raises(AccessError):
        channel.channel_messages(
            dummy_user1['token'], channel2['channel_id'], 0)


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

    assert len(details['all_members']) == 3


def test_join_id(dummy_user1):
    '''
    Testing for an InputError when an invalid channel id is passed into the 
    channel_join function.
    '''

    with pytest.raises(InputError):
        channel.channel_join(dummy_user1['token'], 90439)


def test_join_private(dummy_user1, channel_priv):
    '''
    Testing channel_join function for a private channel.
    '''

    with pytest.raises(InputError):
        channel.channel_join(dummy_user1['token'], channel_priv['channel_id'])


def test_join_member(dummy_user1, channel1):
    '''
    Testing channel_join function when the user is already a member of the channel.
    '''

    with pytest.raises(AccessError):
        channel.channel_join(dummy_user1['token'], channel1['channel_id'])


# ===================================================================================
# testing channel_addowner function.
# ===================================================================================


def test_addowner(dummy_user1, dummy_user3, channel1):
    '''
    Testing basic functionality of the channel_addowner function.
    '''

    channel.channel_addowner(
        dummy_user1['token'], channel1['channel_id'], dummy_user3['u_id'])
    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 3


def test_addowner_owner(dummy_user1, channel1):
    '''
    Checking for InputError when dummy_user1, who is already a member of channel1 tries 
    to call the channel_addowner() function.
    '''

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user1['token'], channel1['channel_id'], dummy_user1['u_id'])


def test_addowner_cid(dummy_user1, dummy_user2, channel1):
    '''
    Checking for InputError when an invalid channel_id is passed into the 
    channel_addowner() function.
    '''

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user1['token'], 39503, dummy_user2['u_id'])


def test_addowner_uid(dummy_user2, dummy_user3, channel2):
    '''
    Checking for InputError when an invalid user id is passed into the 
    channel_addowner() function.
    Checking for InputError when the user id of a user who is not in 
    the channel is passed into channel_addowner()
    '''

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user2['token'], channel2['channel_id'], 898009)

    with pytest.raises(InputError):
        channel.channel_addowner(
            dummy_user2['token'], channel2['channel_id'], dummy_user3['u_id'])


# ===================================================================================
# testing channel_removeowner function.
# ===================================================================================


def test_removeowner(dummy_user1, dummy_user3, channel1):
    '''
    Testing the basic functionality of the channel_removeowner() function.
    '''

    channel.channel_removeowner(
        dummy_user1['token'], channel1['channel_id'], dummy_user3['u_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 2

    # removeowner function should only make a user a non-owner. The total number of
    # users should still be the same.
    assert len(details['all_members']) == 3


def test_removeowner_uid(dummy_user1, dummy_user3, channel1):
    '''
    Checking for InputError when a user who is not an owner of a channel 
    tries to remove another owner.
    '''

    with pytest.raises(InputError):
        channel.channel_removeowner(
            dummy_user3['token'], channel1['channel_id'], dummy_user1['u_id'])

    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    assert len(details['owner_members']) == 2


def test_removeowner_empty(dummy_user1, dummy_user2, channel2):
    pass
