import sys
import jwt
import math
import hashlib
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from email_validation import invalid_email
from datetime import datetime, timedelta, timezone
from data_store import data_store, SECRET
from token_validation import decode_token
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

USER = Blueprint('user', __name__)

@USER.route('/profile', methods='GET')
def user_profile(token, u_id):
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        },
    }

@USER.route('/profile/setname', methods='PUT')
def user_profile_setname(token, name_first, name_last):
    return {
    }

@USER.route('/profile/setemail', methods='PUT')
def user_profile_setemail(token, email):
    return {
    }

@USER.route('/profile/sethandle', methods='PUT')
def user_profile_sethandle(token, handle_str):
    return {
    }