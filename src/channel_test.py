import channel
import channels
import pytest
import auth
from error import InputError
from error import AccessError

# Making a dummy user with valid details.
dummy_user1 = auth.register('something.else@domain.com', 'GreatPassword04', 'something', 'else')
dummy_user2 = auth.register('dummy.user@domain.com', 'BetterPassword09', 'dummy', 'user')

# creating channel and inviting a user. 
c_id1 = channels.create(dummy_user1['token'], 'name1', True)
c_id2 = channels.create(dummy_user2['token'], 'name2', True)

def test_invite_channel():

    # testing channel invite function to non-existent channel.
    channel.invite(dummy_user1['token'], c_id1['channel_id'], dummy_user2['u_id'])

    with pytest.raises(InputError) as e:
        channel.invite(dummy_user1['token'], '3555', dummy_user2['u_id'])


def test_invite_user():
    # testing channel invite for non-existent user.
    with pytest.raises(InputError) as e:
        channel.invite(dummy_user1['token'], c_id1['channel_id'], 69)

    # testing if the user with u_id 1 exists in channel with channel id c_id1.
    details = channel.details(dummy_user1['token'], c_id1['channel_id'])
    user_in_channel = False

    for user in details['all_members']:
        if user['u_id'] == 1:
            user_in_channel = True

    assert user_in_channel == True

def test_invite_access():
    # testing case when inviting user is not a member of a channel.
    
    channel.create(dummy_user2['token'], 'name2', True)
    with pytest.raises(AccessError) as e:
        channel.invite(dummy_user1['token'], c_id2, dummy_user2['u_id'])

    



