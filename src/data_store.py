SECRET = 'the chunts'

# Permission values
OWNER = 1
MEMBER = 2

data_store = {
    'users': [],
    'channels': [],
    'tokens': [],
    'permissions': {
        'owner': OWNER,
        'member': MEMBER
    }
}

EMPTY_DATA_STORE = {
    'users': [],
    'channels': [],
    'tokens': [],
    'permissions': {
        'owner': OWNER,
        'member': MEMBER
    }
}

if __name__ == "__main__":
    pass