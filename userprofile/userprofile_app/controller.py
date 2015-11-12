'''
Controller of the application, which defines the behaviour
of the application when called by the views.
'''

#from flask import current_app

# Exceptions and errors
from flask.ext.api.exceptions import AuthenticationFailed, ParseError
from sqlalchemy.orm.exc import NoResultFound 
from .errors import UsernameExistsException
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
    if db.session.query(User).filter_by(username = username).first() is not None:
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
            

