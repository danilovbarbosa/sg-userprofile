'''
Controller of the application, which defines the behaviour
of the application when called by the views.
'''

import uuid, OpenSSL
from app import app, db, models

import requests 
from requests import RequestException

from flask.ext.api.exceptions import AuthenticationFailed
from flask import render_template

from sqlalchemy.orm.exc import NoResultFound 

from itsdangerous import BadSignature, SignatureExpired


    