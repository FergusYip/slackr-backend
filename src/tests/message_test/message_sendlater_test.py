'''
System testing the functionality of message_sendlater.
Majority of tests performed within message_sendlater where message_send is called.
'''

from time import sleep
from datetime import datetime, timezone
import pytest
import channel
import message
from error import AccessError
from error import InputError

# =====================================================
# ======== TESTING MESSAGE SENDLATER FUNCTION =========
# =====================================================

def test_sendlater(reset, test_channel, test_user):
    '''
    Testing the average case functionality of message_sendlater.
    '''

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_sl_info = message.message_sendlater(test_user['token'],
                                                test_channel['channel_id'], 'Message', time_to_send)

    sleep(2.1)

    message_list = channel.channel_messages(test_user['token'],
                                            test_channel['channel_id'], 0)

    assert message_list['messages'][0]['message_id'] == message_sl_info['message_id'] == 1
    assert message_list['messages'][0]['message'] == 'Message'


def test_sendlater_messageid_order(reset, test_channel, test_user):
    '''
    Testing the order in which message_ids are allocated while a
    sendlater request is waiting until it sends.
    '''

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_sl_info = message.message_sendlater(test_user['token'],
                                                test_channel['channel_id'], 'Message', time_to_send)

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    sleep(2.1)

    message_list = channel.channel_messages(test_user['token'], test_channel['channel_id'], 0)

    # Whilst the message_send function sent first, the earlier message ID was allocated
    # to message_sendlaetr, as the request was processed first. But the order in the
    # channel is first: message_send second: message_sendlater.
    assert message_list['messages'][0]['message_id'] == message_info['message_id'] == 2
    assert message_list['messages'][1]['message_id'] == message_sl_info['message_id'] == 1

def test_sendlater_timeinpast(reset, test_channel, test_user):
    '''
    Testing that an InputError will be raised if the user attempts to make
    a sendlater request for a time that is in the past.
    '''

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now - 2

    with pytest.raises(InputError):
        message.message_sendlater(test_user['token'], test_channel['channel_id'], 'Message',
                                  time_to_send)

def test_sendlater_invalid_token(reset, test_channel, invalid_token):
    '''
    Testing that attempting to use message_sendlater with an invalid token will
    raise an AccessError.
    '''

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    with pytest.raises(AccessError):
        message.message_sendlater(invalid_token, test_channel['channel_id'], 'Message',
                                  time_to_send)
