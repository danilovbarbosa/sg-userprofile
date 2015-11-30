'''
Models that extend the Model class provided by 
Flask's SQLAlchemy extension (flask.ext.sqlalchemy).
'''

#from flask import current_app
from .extensions import db

import datetime

from uuid import UUID
import OpenSSL
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    """Model "users" table in the database. 
    It contains id, a username, and hashed password. 
    The same user may have many sessions; a session can have only one user.
    """
    
    __tablename__ = "user"    
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    sessions = db.relationship("Session", backref = db.backref('user', lazy="joined"), lazy = "dynamic")
    
    def __init__(self, username, password):
        """Initialize client class with the data provided, and encrypting password."""
        self.id = UUID(bytes = OpenSSL.rand.bytes(16)).hex
        self.username = username
        self.password_hash = pwd_context.encrypt(password)
        #self.token = None
        
    def as_dict(self):
        """Returns a representation of the object as dictionary."""
        sessions_list = []
        for session in self.sessions:
            sessions_list.append(session.as_dict())
            
        obj_d = {
            'id': self.id,
            'username': self.username,
            'sessions':sessions_list
        }
        return obj_d
    
    def verify_password(self, password):
        """Checks if the username's password is valid. Returns boolean."""
        #LOG.debug("Checking apikey... clientid %s, apikey %s" % (self.clientid, apikey))
        verified = pwd_context.verify(password, self.password_hash)
        if verified:
            #g.clientid = self.clientid
            return True
        else:
            return False

    
class Session(db.Model):
    """Model "sessions" table in the database. 
    The same user may have many sessions; a session can have only one user.
    """
    
    __tablename__ = "session"    
    id = db.Column(db.String(36), primary_key=True)
    timestamp = db.Column(db.DateTime(True))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    active = db.Column(db.Boolean)
    #user = db.relationship("User", backref="session", lazy="join")
    
    def __init__(self, user):
        """Initializes the session for a user"""
        self.id = UUID(bytes = OpenSSL.rand.bytes(16)).hex
        self.timestamp = datetime.datetime.utcnow()
        self.user_id = user.id
        self.active = True
        
    def as_dict(self):
        """Returns a representation of the object as dictionary."""
        obj_d = {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'user': [{
                      'id':self.user.id,
                      'username':self.user.username,
                      'active':str(self.active)
                }],
        }
        return obj_d
    
