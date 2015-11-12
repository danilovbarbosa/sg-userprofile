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
    #user = db.session.query(User).filter_by(username = username).one()
    return user

def get_user_from_sessionid(sessionid):
    """Auxiliary function for the view, to retrieve a user object from a userid."""
    try: 
        gamingsession = Session.query.get(sessionid)
        try:
            user = User.query.get(gamingsession.user_id)
            return user
        except NoResultFound:
            LOG.warning("Username was deleted while sessionid was still active? Remove sessionid.")
            expire_session(sessionid)
            raise UserNotFoundException("Username associated with this record is not in database.")
    except NoResultFound:
        raise SessionidNotFoundException("Sessionid not in database.")
    
            
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
    session = Session.query(sessionid)
    #session = db.session.query(Session).filter_by(id = sessionid).one()
    return session


def new_session(username):
    """Takes a username and returns a new session id."""
    #First, get the userid from the username
    user = get_user(username)
    session = Session(user.id)
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
   
def expire_session(sessionid):
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
    