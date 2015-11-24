'''
Defines the methods/endpoints (the views) of the userprofile service.
This defines the interaction points, but the actual logic is treated
by the :mod:`controller`.
'''

#Flask and modules
from flask import Blueprint, jsonify, request
from flask.ext.api import status 
#from flask.helpers import make_response

#Exceptions and errors
from flask.ext.api.exceptions import AuthenticationFailed, ParseError
from sqlalchemy.orm.exc import NoResultFound
from .errors import *

#Python modules
#import datetime
#import json
#import time

#Import controller
from userprofile_app import controller


#Extensions
#from .extensions import LOG, db

#Userprofile blueprint
userprofile = Blueprint('userprofile', __name__, url_prefix='/userprofile/api/v1.0')

######################################################
# Handshake
######################################################

@userprofile.route('/version')
def get_version():
    return jsonify({'data': [{'version':'v1.0'}] }), status.HTTP_200_OK

######################################################
# user management
######################################################

@userprofile.route('/users', methods = ['POST'])
def new_user():
    """Creates a new user with the data received from a request.    
    """
    #Check if request is json and contains all the required fields
    required_fields = ["username", "password"]
    if not request.json or not (set(required_fields).issubset(request.json)): 
        return jsonify({'message': 'Invalid request. Please try again.'}), status.HTTP_400_BAD_REQUEST
    else:
        try:
            username = request.json["username"]
            password = request.json["password"]
            controller.create_user(username, password)
            return jsonify({ 'message': "User created successfully." }), status.HTTP_201_CREATED
        except AuthenticationFailed:
            return jsonify({'message': 'Could not authenticate. Check your credentials.'}), status.HTTP_401_UNAUTHORIZED 
        except UsernameExistsException:
            return jsonify({'message': 'Username already in database.'}), status.HTTP_409_CONFLICT 
        except ParseError:
            return jsonify({'message': 'Invalid parameters.'}), status.HTTP_400_BAD_REQUEST
        

######################################################
# Session
######################################################

@userprofile.route('/sessions', methods = ['POST'])
def new_session():
    """ If the credentials are valid, create a new session id and returns its id.    
    """
    #Check if request is json and contains all the required fields
    required_fields = ["username", "password"]
    if not request.json or not (set(required_fields).issubset(request.json)): 
        return jsonify({'message': 'Invalid request. Please try again.'}), status.HTTP_400_BAD_REQUEST
    else:
        try:
            username = request.json["username"]
            password = request.json["password"]
            user = controller.user_authenticate(username, password)
            action = "get_session"
            if (controller.is_authorized(user, action)):
                new_sessionid = controller.new_session(username)
            return jsonify({'sessionid': new_sessionid}), status.HTTP_200_OK
        except AuthenticationFailed:
            return jsonify({'errors': [{'userMessage':'Invalid credentials.'}]}), status.HTTP_401_UNAUTHORIZED  

@userprofile.route('/sessions/<sessionid>')
def get_sessioninfo(sessionid):
    """TODO: Implement some kind of authentication and permission system here to 
    restrict access to retrieving user information from a sessionid."""
#     required_fields = ["sessionid"]
#     if not request.json or not (set(required_fields).issubset(request.json)): 
#         return jsonify({'message': 'Invalid request. Please try again.'}), status.HTTP_400_BAD_REQUEST
#     else:
    if not controller._is_uuid_valid(sessionid):
        return jsonify({'errors': [{'userMessage':'Invalid request. Please try again.'}]}), status.HTTP_400_BAD_REQUEST
    else:
        try:
            session = controller.get_session(sessionid)   
            
            return jsonify(session.as_dict()), status.HTTP_200_OK
        except UserNotFoundException as e:
            return jsonify({'errors': [{'userMessage':'User not found.'}]}), status.HTTP_404_NOT_FOUND
        except SessionidNotFoundException as e:
            return jsonify({'errors': [{'userMessage':'SessionID not found.'}]}), status.HTTP_404_NOT_FOUND
        except AuthenticationFailed:
            return jsonify({'errors': [{'userMessage':'Invalid credentials.'}]}), status.HTTP_401_UNAUTHORIZED  
        
# @userprofile.route('/session/<sessionid>')
# def get_sessioninfo(sessionid):
#     try:
#         session = controller.get_session(sessionid)
#         return jsonify({'message':"Success.", 'result': session.as_dict()}), status.HTTP_200_OK
#     except SessionidNotFoundException as e:
#         return jsonify({'message': e.value, "result":""}), status.HTTP_200_OK
#     except AuthenticationFailed:
#         return jsonify({'message': "Invalid credentials."}), status.HTTP_401_UNAUTHORIZED  
    