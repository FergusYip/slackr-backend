import channel
import channels
import pytest
import auth
from error import InputError
from error import AccessError

# Making a dummy user with valid details.
dummy_user1 = auth.register(
    'something.else@domain.com', 'GreatPassword04', 'something', 'else')
dummy_user2 = auth.register(
    'dummy.user@domain.com', 'BetterPassword09', 'dummy', 'user')

# creating channels.
c_id1 = channels.create(dummy_user1['token'], 'name1', True)
c_id2 = channels.create(dummy_user2['token'], 'name2', True)

# ===================================================================================
# testing channel_invite function.
# ===================================================================================


def test_invite_channel():

    # testing channel invite function to valid channel.
    channel.invite(dummy_user1['token'],
                   c_id1['channel_id'], dummy_user2['u_id'])

    # testing channel invite function to invalid channel.
    with pytest.raises(InputError) as e:
        channel.invite(dummy_user1['token'], '3555', dummy_user2['u_id'])


def test_invite_user():
    # testing channel invite for non-existent user.
    with pytest.raises(InputError) as e:
        channel.invite(dummy_user1['token'], c_id1['channel_id'], 69)

    # testing if the user with user id dummy_user2[u_id] exists in channel c_id1.
    # this should pass if line 19 executed.
    details = channel.details(dummy_user1['token'], c_id1['channel_id'])
    user_in_channel = False

    for user in details['all_members']:
        if user['u_id'] == dummy_user2['u_id']:
            user_in_channel = True

    assert user_in_channel == True


def test_invite_access():
    # testing case when inviting user is not a member of a channel.
    # at this point - the channel name1 has both users (dummy_user1 and dummy_user2)
    # but the channel name2 only has dummy_user2.
    with pytest.raises(AccessError) as e:
        channel.invite(dummy_user1['token'], c_id2, dummy_user2['u_id'])


# ===================================================================================
# testing channel_details function.
# ===================================================================================


def test_details_owner():
    # Checking if channel name1 has dummy_user1 in owner_members.
    details = channel.details(dummy_user1['token'], c_id1['channel_id'])
    owner = False

    for user in details['owner_members']:
        if user['u_id'] == dummy_user1['u_id']:
            owner = True

    assert owner == True


def test_details_all():
    # Checking if channel name1 has 2 users in all_members.
    details = channel.details(dummy_user1['token'], c_id1['channel_id'])
    size = 0

    for user in details['all_members']:
        size += 1

    assert size == 2


def test_details_invalid():
    # Testing case when channel ID is invalid.
    with pytest.raises(InputError) as e:
        channel.details(dummy_user1['token'], 42045)
