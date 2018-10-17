'''
Defines the methods/endpoints (the views) of the userprofile service.
This defines the interaction points, but the actual logic is treated
by the :mod:`controller`.
'''

#Flask and modules
from flask import Blueprint, jsonify, request, make_response
from flask.ext.api import status 
#from flask.helpers import make_response

#Exceptions and errors
from flask.ext.api.exceptions import AuthenticationFailed, ParseError
#from sqlalchemy.orm.exc import NoResultFound
from .errors import *

#Python modules
#import datetime
#import json
#import time
import simplejson

#Import controller
from userprofile_app import controller


#Extensions
from .extensions import LOG

#Userprofile blueprint
userprofile = Blueprint('userprofile', __name__, url_prefix='/v1')

######################################################
# Handshake
######################################################


@userprofile.route('/')
@userprofile.route('/index')
@userprofile.route('/home')
def index():
    return "testando 123, testando"



@userprofile.route('/version')
def get_version():
    '''
    Returns the current version of the API.
    '''
    return jsonify(version='v1'), status.HTTP_200_OK

######################################################
# user management
######################################################

@userprofile.route('/users/<userid>')
def get_user(userid):
    error={}
    error["message"] = "Forbidden" 
    error["code"] = 403
    return jsonify(error=error), status.HTTP_403_FORBIDDEN
    
@userprofile.route('/users', methods = ['POST'])
def new_user():
    '''
    Creates a new user with the data received from a request. 
    
    :<json string username: 
    :<json string password: 
    :status 201: Successful request
    :status 400: Not JSON object or missing parameters
    :status 401: Wrong credentials
    '''
    #Check if request is json and contains all the required fields
    required_fields = ["username", "password"]
    
    error = {}
    
    if not request.json or not (set(required_fields).issubset(request.json)): 
        error["message"] = "Invalid request." 
        error["code"] = 400
        return jsonify(error=error), status.HTTP_400_BAD_REQUEST
    
    else:
        
        
        try:
            username = request.json["username"]
            password = request.json["password"]

            #############################
            # Success
            #############################

            user = controller.create_user(username, password)
            user_response= simplejson.dumps(user.as_hateoas(), indent=2)
            
            response = make_response(user_response, status.HTTP_201_CREATED)
            response.headers["X-Total-Count"] = 1
            response.headers["Content-Type"] = "application/json"
            
            return response
            
        except AuthenticationFailed:
            error["message"] = "Could not authenticate. Check your credentials." 
            error["code"] = 401
            return jsonify(error=error), status.HTTP_401_UNAUTHORIZED
        
        except UsernameExistsException:
            error["message"] = "Username already in database." 
            error["code"] = 409
            return jsonify(error=error), status.HTTP_409_CONFLICT
                
        except ParseError:
            error["message"] = "Invalid parameters." 
            error["code"] = 400
            return jsonify(error=error), status.HTTP_400_BAD_REQUEST
        

######################################################
# Session
######################################################

@userprofile.route('/sessions', methods = ['POST'])
def new_session():
    '''
    Creates a new gaming session. Requires authentication by providing a valid username/password.
    
    TODO: Switch to token authentication
     
    :<json string username: Username of the user who is using the session 
    :<json string password: Password for authenticating
    :status 201: Successful request
    :status 400: Not JSON object or missing parameters
    :status 401: Wrong credentials
    '''
    #Check if request is json and contains all the required fields
    required_fields = ["username", "password"]
    
    error = {}
    
    if not request.json or not (set(required_fields).issubset(request.json)):
        error["message"] = "Invalid request." 
        error["code"] = 400
        return jsonify(error=error), status.HTTP_400_BAD_REQUEST
    
    else:
        try:
            
            #############################
            # Success
            #############################
            
            username = request.json["username"]
            password = request.json["password"]
            
            user = controller.user_authenticate(username, password)
            
            action = "get_session"
            
            if (controller.is_authorized(user, action)):
                
                
                gamingsession = controller.new_session(username)
                gamingsession_response = simplejson.dumps(gamingsession.as_hateoas(), indent=2)
                response = make_response(gamingsession_response, status.HTTP_201_CREATED)
                response.headers["X-Total-Count"] = 1
                response.headers["Content-Type"] = "application/json"
                
                return response
                #return jsonify({'sessionid': new_sessionid}), status.HTTP_201_CREATED
                
            else:
                error["message"] = "You are not authorized to perform this action." 
                error["code"] = 401
                return jsonify(error=error), status.HTTP_401_UNAUTHORIZED
            
            
        
        except AuthenticationFailed:
            error["message"] = "Could not authenticate. Check your credentials." 
            error["code"] = 401
            return jsonify(error=error), status.HTTP_401_UNAUTHORIZED


@userprofile.route('/sessions/<sessionid>')
def get_session(sessionid):
    '''
    Get information about the sessionid.
    
    TODO: Implement some kind of authentication and permission system here to 
    restrict access to retrieving user information from a sessionid.
    
    :param sessionid:
    :status 200: Successful request
    :status 400: Not JSON object or missing parameters
    :status 401: Wrong credentials
    :status 404: Sessionid does not exist
    '''

#     required_fields = ["sessionid"]
#     if not request.json or not (set(required_fields).issubset(request.json)): 
#         return jsonify({'message': 'Invalid request. Please try again.'}), status.HTTP_400_BAD_REQUEST
#     else:

    error = {}
    
    if not controller._is_uuid_valid(sessionid):
        error["message"] = "Invalid request." 
        error["code"] = 400
        return jsonify(error=error), status.HTTP_400_BAD_REQUEST
    
    else:
        session = {}
        inactive = False
        if ("inactive" in request.args):
            if request.args["inactive"].lower() == "true":
                inactive = True
        try:
            
            #############################
            # Success
            #############################
            
            gamingsession = controller.get_session(sessionid, inactive) 
            
            gamingsession_response = simplejson.dumps(gamingsession.as_hateoas(), indent=2)
            response = make_response(gamingsession_response, status.HTTP_200_OK)
            response.headers["X-Total-Count"] = 1
            response.headers["Content-Type"] = "application/json"
            
            return response

             
        except UserNotFoundException:
            error["message"] = "User not found." 
            error["code"] = 404
            return jsonify(error=error), status.HTTP_404_NOT_FOUND 
                
        except SessionidNotFoundException:
            error["message"] = "SessionID not found." 
            error["code"] = 404
            return jsonify(error=error), status.HTTP_404_NOT_FOUND 
      
        except AuthenticationFailed:
            error["message"] = "Could not authenticate. Check your credentials." 
            error["code"] = 401
            return jsonify(error=error), status.HTTP_401_UNAUTHORIZED  
            
        
        
        
        
@userprofile.route('/sessions/<sessionid>', methods = ['DELETE'])
def delete_session(sessionid):
    '''
    Marks the session as inactive.
    
    TODO: Implement some kind of authentication and permission system here to 
    restrict access to deleting a sessionid.
    
    :param sessionid:
    :status 204: Deleted successfully
    :status 400: Bad parameters (badly formed sessionid)
    :status 401: Wrong credentials
    :status 404: Sessionid does not exist
    '''
    error = {}
    
    if not controller._is_uuid_valid(sessionid):
        error["message"] = "Invalid request." 
        error["code"] = 400
        return jsonify(error=error), status.HTTP_400_BAD_REQUEST
    
    else:
        try:
            #############################
            # Success
            #############################
            
            controller.delete_session(sessionid)  
                      
            return "", status.HTTP_204_NO_CONTENT
        
        
        except SessionidNotFoundException:
            error["message"] = "SessionID not found." 
            error["code"] = 404
            return jsonify(error=error), status.HTTP_404_NOT_FOUND 
        
        except AuthenticationFailed:
            error["message"] = "Could not authenticate. Check your credentials." 
            error["code"] = 401
            return jsonify(error=error), status.HTTP_401_UNAUTHORIZED   
        
