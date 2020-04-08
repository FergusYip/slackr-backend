'''Creating the error objects to be raised.'''

from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    '''
    AccessErrors are present when an unauthorized user attempts
    to access/alter/remove data that they are not permitted to.
    '''

    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    '''
    InputErrors are present when incorrect parameters are entered into
    the function request.
    '''

    code = 400
    message = 'No message specified'
