'''
Models that extend the Model class provided by 
Flask's SQLAlchemy extension (flask.ext.sqlalchemy).
'''

from flask import current_app
from .extensions import db

import datetime

from uuid import UUID
import OpenSSL
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    """Model "users" table in the database. 
    It contains id, a username, and hashed password. 
    """
    
    __tablename__ = "user"    
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    
    def __init__(self, username, password):
        """Initialize client class with the data provided, and encrypting password."""
        self.id = UUID(bytes = OpenSSL.rand.bytes(16)).hex
        self.username = username
        self.password_hash = pwd_context.encrypt(password)
        #self.token = None
        
    def as_dict(self):
        """Returns a representation of the object as dictionary."""
        obj_d = {
            'id': self.id,
            'username': self.username,
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
    It contains id, a username, and hashed password. 
    """
    
    __tablename__ = "session"    
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(True))
    
    def __init__(self, user_id):
        """Initializes the session for a user"""
        self.id = UUID(bytes = OpenSSL.rand.bytes(16)).hex
        self.user_id = user_id
        self.timestamp = datetime.datetime.utcnow()
        
    def as_dict(self):
        """Returns a representation of the object as dictionary."""
        obj_d = {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        return obj_d
    
