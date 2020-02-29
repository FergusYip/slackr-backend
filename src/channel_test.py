import channel
import channels
import pytest
import auth

def test_invite():

    # Making a dummy user with valid details.
    dummy_user = auth.register('something.else@domain.com', 'GreatPassword04', 'something', 'else')

    # creating channel and inviting a user. 
    c_id = channels.create(dummy_user['token'], 'name1', True)
    channel.invite(dummy_user['token'], c_id['channel_id'], dummy_user['u_id'])

    # testing channel invite function to non-existent channel.
    with pytest.raises(InputError) as e:
        channel.invite(dummy_user['token'], '3555', dummy_user['u_id'])

    # testing channel invite for non-existent user.
    with pytest.raises(InputError) as e:
        channel.invite(dummy_user['token'], c_id['channel_id'], 69)

    # testing if the user with u_id 1 exists in channel with channel id c_id.
    details = channel.details(dummy_user['token'], c_id['channel_id'])
    user_in_channel = False

    for user in details['all_members']:
        if user['u_id'] == 1:
            user_in_channel = True

    assert user_in_channel == True

    # Testing case when 

    



