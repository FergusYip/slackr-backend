import user
import channel
import channels
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ========== TESTING MESSAGE SEND FUNCTION ============
# =====================================================

def test_averagecase_uid():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    profile_information = user.profile(new_user['token'], new_user['u_id'])
    assert(new_user['u_id'] == profile_information['user']['u_id'])

def test_averagecase_email():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    profile_information = user.profile(new_user['token'], new_user['u_id'])
    assert('test@test.com' == profile_information['user']['email'])

def test_averagecase_firstname():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    profile_information = user.profile(new_user['token'], new_user['u_id'])
    assert('Lorem' == profile_information['user']['name_first'])

def test_averagecase_lastname():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    profile_information = user.profile(new_user['token'], new_user['u_id'])
    assert('Ipsum' == profile_information['user']['name_last'])

def test_averagecase_handle():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    profile_information = user.profile(new_user['token'], new_user['u_id'])
    assert('lipsum' == profile_information['user']['handle_str'])

def test_inputError():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(InputError) as e:
        user.profile(new_user['token'], 'NOTAUID')
