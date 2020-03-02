# Assumptions

## auth.py
* Token provided by *auth_login* and *auth_register* are unique to the login session
* Password length could be upwards of 32 characters
* Passwords will only consist of ASCII printable characters
* Email addresses are validated using the method in the GeeksforGeeks article as opposed to RFC documents
* A user may have multiple active sessions at once

### auth_login
* Unable to test whether *auth_login* is able to handle invalid emails since no user is registered with an invalid email.