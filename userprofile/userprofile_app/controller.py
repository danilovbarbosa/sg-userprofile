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
    """Creates a new user with given username and password."""
    #Check if username already exists
    if ( (username is None) or (username=="") or (password is None) or (password=="") ):
        raise ParseError('Invalid parameters')
    if User.query.filter_by(username = username).first() is not None:
        raise UsernameExistsException('Client exists')
    
    new_user = User(username, password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return True
    except Exception as e:
        LOG.warning(e)
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        LOG.error(e, exc_info=True)
        raise e      
    
def get_user(username):
    """Auxiliary function for the view, to retrieve a user object from a username."""
    user = User.query.filter_by(username = username).one()
    return user
    
            
def user_authenticate(username, password):
    """Tries to authenticate a user by checking a username/password pair."""
    try:
        user = User.query.filter_by(username = username).one()
        if (not user.verify_password(password)):
            raise AuthenticationFailed("Wrong credentials.")
        else:
            return user
    except NoResultFound:
        raise AuthenticationFailed("Username does not exist.")
    
def is_authorized(user, action):
    """Verifies if this user is allowed to request this action.
    TODO: Implement this or use ACL."""
    return True

###################################################
#    Session functions
###################################################

def get_session(sessionid):
    """Auxiliary function for the view, to retrieve a session object from a sessionid."""
    session = Session.query.get(sessionid)
    if session:
        return session
    else:
        raise SessionidNotFoundException


def new_session(username):
    """Takes a username and returns a new session id."""
    #First, get the userid from the username
    user = get_user(username)
    session = Session(user)
    try:
        db.session.add(session)
        db.session.commit()
        return session.id
    except Exception as e:
        LOG.warning(e)
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        LOG.error(e, exc_info=True)
        raise e    
   
def delete_session(sessionid):
    session = get_session(sessionid)
    try:
        db.session.delete(session)
        db.session.commit()
    except Exception as e:
        LOG.warning(e)
        db.session.rollback()
        db.session.flush() # for resetting non-commited .delete()
        LOG.error(e, exc_info=True)
        raise e
    
def _is_uuid_valid(sessionid):
    """
    Validate that a UUID string is in
    fact a valid uuid.
    """

    try:
        val = UUID(sessionid)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    return val.hex == sessionid
    