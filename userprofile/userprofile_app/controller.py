'''
Controller of the application, which defines the behaviour
of the application when called by the views.
'''

#from flask import current_app

# Exceptions and errors
from flask.ext.api.exceptions import AuthenticationFailed, ParseError
from sqlalchemy.orm.exc import NoResultFound 
from .errors import *
#from itsdangerous import BadSignature, SignatureExpired
#from werkzeug.exceptions import Unauthorized
#from flask_api.exceptions import NotFound

from uuid import UUID



# Models
from userprofile_app.models import User, Session

#Extensions
from .extensions import db, LOG


###################################################
#    User functions
###################################################

def create_user(username, password):
    '''
    Creates a new user with given username and password.
    
    :param username:
    :param password:
    '''
    
    #Check if username already exists
    if ( (username is None) or (username=="") or (password is None) or (password=="") ):
        raise ParseError('Invalid parameters')
    if User.query.filter_by(username = username).first() is not None:  # @UndefinedVariable
        raise UsernameExistsException('Client exists')
    
    new_user = User(username, password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return new_user
    except Exception as e:
        LOG.warning(e)
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        LOG.error(e, exc_info=True)
        raise e      
    
def get_user(username):
    '''
    Auxiliary function for the view, to retrieve a user object from a username.
    
    :param username:
    '''
    
    user = User.query.filter_by(username = username).one()  # @UndefinedVariable
    return user


def get_user_with_id(id_user):
    '''
    Auxiliary function for the view, to retrieve a user object from a username.

    :param username:
    '''

    user = User.query.filter_by(id=id_user).one()  # @UndefinedVariable
    return user
    
            
def user_authenticate(username, password):
    '''
    Tries to authenticate a user by checking a username/password pair.
    
    :param username:
    :param password:
    '''
    
    try:
        user = User.query.filter_by(username = username).one()  # @UndefinedVariable
        if (not user.verify_password(password)):
            raise AuthenticationFailed("Wrong credentials.")
        else:
            return user
    except NoResultFound:
        raise AuthenticationFailed("Username does not exist.")
    
def is_authorized(user, action):
    '''
    Verifies if this user is allowed to request this action.
    
    TODO: Implement this or use ACL.
    
    :param user:
    :param action:
    '''

    return True

###################################################
#    Session functions
###################################################

def get_session(sessionid, search_inactives=False):
    '''
    Auxiliary function for the view, to retrieve a session object from a sessionid.
    
    :param sessionid:
    :param search_inactives:
    '''
    
    if (search_inactives==False):
        try:
            session = Session.query.filter_by(id=sessionid,active=True).one()  # @UndefinedVariable
        except NoResultFound:
            session = False
    else:
        try:
            session = Session.query.filter_by(id=sessionid).one()  # @UndefinedVariable
        except NoResultFound:
            session = False
        
    if session:
        return session
    else:
        raise SessionidNotFoundException("Session does not exist.")


def new_session(username):
    '''
    Takes a username and returns a new session id.
    
    :param username:
    '''
    
    #First, get the userid from the username
    user = get_user(username)
    session = Session(user)
    try:
        db.session.add(session)
        db.session.commit()
        return session
    except Exception as e:
        LOG.warning(e)
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        LOG.error(e, exc_info=True)
        raise e    
   
def delete_session(sessionid):
    session = get_session(sessionid)
    
    try:
        #db.session.delete(session)
        session.active = False
        db.session.commit()
    except Exception as e:
        LOG.warning(e)
        db.session.rollback()
        db.session.flush() # for resetting non-commited .delete()
        LOG.error(e, exc_info=True)
        raise e
    
def _is_uuid_valid(sessionid):
    '''
    Validate that a UUID string is in fact a valid uuid.
    
    :param sessionid:
    '''
    
    try:
        val = UUID(sessionid)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    return val.hex == sessionid
    