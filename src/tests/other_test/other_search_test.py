'''System tests for search'''
import pytest
import channel
import message
import other
from error import AccessError


def test_search_no_channel(reset, test_user):  # pylint: disable=W0613
    '''Test search function when there is no channel'''

    assert len(other.search(test_user['token'], '')['messages']) == 0


def test_search_empty_channel(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test search function when channel has no messages'''

    test_channel = new_channel(test_user, 'Channel')
    assert len(other.search(test_user['token'], '')['messages']) == 0


def test_search_return_type(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test the types of values returned by search'''

    test_channel = new_channel(test_user, 'Channel')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')

    results = other.search(test_user['token'], 'Hello')['messages'][0]
    assert isinstance(results, dict)
    assert isinstance(results['message_id'], int)
    assert isinstance(results['u_id'], int)
    assert isinstance(results['message'], str)
    assert isinstance(results['time_created'], int)


def test_search_single_channel(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test that the sole message is returned by search'''

    test_channel = new_channel(test_user, 'Channel')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')

    msg_in_channel = channel.channel_messages(test_user['token'],
                                              test_channel['channel_id'],
                                              0)['messages'][0]
    msg_in_search = other.search(test_user['token'], 'Hello')['messages'][0]

    assert msg_in_channel == msg_in_search


def test_search_multiple_messages(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test search with multiple unique messages'''

    test_channel = new_channel(test_user, 'Channel')

    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Alpha')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Bravo')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Charlie')

    assert len(other.search(test_user['token'], 'a')['messages']) == 3
    assert len(other.search(test_user['token'], 'b')['messages']) == 1
    assert len(other.search(test_user['token'], 'Romeo')['messages']) == 0


def test_search_multiple_channels(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test that search works on multiple channels'''

    ch1 = new_channel(test_user, 'Channel 1')
    message.message_send(test_user['token'], ch1['channel_id'], 'Channel 1')

    ch2 = new_channel(test_user, 'Channel 2')
    message.message_send(test_user['token'], ch2['channel_id'], 'Channel 2')

    ch3 = new_channel(test_user, 'Channel 3')
    message.message_send(test_user['token'], ch3['channel_id'], 'Channel 3')

    assert len(other.search(test_user['token'], 'Channel')['messages']) == 3


def test_search_unauthorised_channels(reset, new_user, new_channel):  # pylint: disable=W0613
    '''Test that users cannot search unauthorised channels'''

    tom = new_user('tom@email.com')

    jerry = new_user('jerry@email.com')
    mice_ch = new_channel(jerry, 'Mice Only')

    message.message_send(jerry['token'], mice_ch['channel_id'],
                         'Tom can\'t see this')

    assert len(other.search(jerry['token'], '')['messages']) == 1
    assert len(other.search(tom['token'], '')['messages']) == 0


def test_search_case_insensitive(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test that query string is not case sensitive'''

    test_channel = new_channel(test_user, 'Channel')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')
    msg_in_channel = channel.channel_messages(test_user['token'],
                                              test_channel['channel_id'],
                                              0)['messages'][0]
    msg_in_search = other.search(test_user['token'], 'hello')['messages'][0]
    assert msg_in_channel == msg_in_search


def test_search_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test search function with invalid token'''

    with pytest.raises(AccessError):
        other.search(invalid_token, '')
