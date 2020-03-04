import channel
import channels
import pytest
import auth
from error import InputError
from error import AccessError


@pytest.fixture
def dummy_user1():
    dummy_user1 = auth.auth_register(
        'something.else@domain.com', 'GreatPassword04', 'something', 'else')
    return dummy_user1


@pytest.fixture
def dummy_user2():
    dummy_user2 = auth.auth_register(
        'dummy.user@domain.com', 'BetterPassword09', 'dummy', 'user')
    return dummy_user2


@pytest.fixture
def channel1(dummy_user1):
    c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
    return c_id1


@pytest.fixture
def channel2(dummy_user2):
    c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)
    return c_id2

# # Making a dummy user with valid details.
# dummy_user1 = auth.auth_register(
#     'something.else@domain.com', 'GreatPassword04', 'something', 'else')
# dummy_user2 = auth.auth_register(
#     'dummy.user@domain.com', 'BetterPassword09', 'dummy', 'user')

# # creating channels.
# c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
# c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)

# ===================================================================================
# testing channel_invite function.
# ===================================================================================


def test_invite_channel(dummy_user1, dummy_user2, channel1):

    # testing channel invite function to valid channel.channel_
    channel.channel_invite(
        dummy_user1['token'], channel1['channel_id'], dummy_user2['u_id'])

    # testing channel invite function to invalid channel.channel_
    with pytest.raises(InputError) as e:
        channel.channel_invite(
            dummy_user1['token'], '3555', dummy_user2['u_id'])


def test_invite_user(dummy_user1, dummy_user2, channel1):
    # testing channel invite for non-existent user.
    with pytest.raises(InputError) as e:
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
    # testing case when inviting user is not a member of a channel.channel_
    # at this point - the channel name1 has both users (dummy_user1 and dummy_user2)
    # but the channel name2 only has dummy_user2.
    with pytest.raises(AccessError) as e:
        channel.channel_invite(
            dummy_user1['token'], channel2, dummy_user2['u_id'])


# ===================================================================================
# testing channel_details function.
# ===================================================================================


def test_details_owner(dummy_user1, channel1):
    # Checking if channel name1 has dummy_user1 in owner_members.
    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])
    owner = False

    for user in details['owner_members']:
        if user['u_id'] == dummy_user1['u_id']:
            owner = True

    assert owner == True


def test_details_added_owner(dummy_user1, dummy_user2, channel1):
    # Adding another owner (dummy_user2) to name1 and checking if the channel
    # has 2 owners.
    channel.channel_addowner(
        dummy_user1['token'], channel1['channel_id'], dummy_user2['u_id'])
    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])

    size = 0

    for user in details['owner_members']:
        size += 1

    assert size == 2


def test_details_all(dummy_user1, channel1):
    # Checking if channel name1 has 2 users in all_members.
    details = channel.channel_details(
        dummy_user1['token'], channel1['channel_id'])
    size = 0

    for user in details['all_members']:
        size += 1

    assert size == 2


def test_details_invalid(dummy_user1, channel2):
    # Testing case when channel ID is invalid.
    with pytest.raises(InputError) as e:
        channel.channel_details(dummy_user1['token'], 42045)

    # Testing case when user asking for details isn't part of the channel.channel_
    # at this point, channel name2 has only dummy_user2 as members.
    # testing case when dummy_user1 asks for details about channel name2.
    with pytest.raises(AccessError) as e:
        channel.channel_details(dummy_user1['token'], channel2['channel_id'])


# ===================================================================================
# testing channel_messages function.
# ===================================================================================
