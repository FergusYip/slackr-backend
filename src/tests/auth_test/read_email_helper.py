'''Email reading function from Geeks for Geeks
https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/'''

import imaplib

USER = 'thechunts.slackr@gmail.com'
PASSWORD = 'chuntsslackr'
IMAP = 'imap.gmail.com'


def get_body(msg):
    '''Function to get email content part i.e its body part'''
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def search(key, value, con):
    '''Function to search for a key value pair'''
    data = con.search(None, key, '"{}"'.format(value))[1]
    return data


def get_emails(result_bytes, connection):
    '''Function to get the list of emails under this label'''
    messages = []  # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        data = connection.fetch(num, '(RFC822)')[1]
        messages.append(data)

    return messages


def get_num_emails_from_chunts():
    '''Get the number of email recieved that are from thechunts.slackr@gmail.com'''

    # this is done to make SSL connnection with GMAIL
    connection = imaplib.IMAP4_SSL(IMAP)

    # logging the user in
    connection.login(USER, PASSWORD)

    # calling function to check for email under this label
    connection.select('Inbox')

    # fetching emails from same email as user
    msgs = get_emails(search('FROM', USER, connection), connection)

    return len(msgs)


def delete_all_emails():
    '''Delete all emails from imbox'''

    # this is done to make SSL connnection with GMAIL
    connection = imaplib.IMAP4_SSL(IMAP)

    # logging the user in
    connection.login(USER, PASSWORD)

    # calling function to check for email under this label
    connection.select('Inbox')

    connection.store('1', '+X-GM-LABELS', '\\Trash')


if __name__ == '__main__':
    pass