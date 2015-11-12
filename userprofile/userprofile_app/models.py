'''
Models that extend the Model class provided by 
Flask's SQLAlchemy extension (flask.ext.sqlalchemy).
'''

from flask import current_app
from .extensions import db

from uuid import UUID
import OpenSSL
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    """Model "users" table in the database. 
    It contains id, a username, and hashed password. 
    """
    
    __tablename__ = "user"    
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    
    def __init__(self, username, password):
        """Initialize client class with the data provided, and encrypting password."""
        self.id = UUID(bytes = OpenSSL.rand.bytes(16)).hex
        self.username = username
        self.password_hash = pwd_context.encrypt(password)
        #self.token = None

    
class Session(db.Model):
    """Model "sessions" table in the database. 
    It contains id, a username, and hashed password. 
    """
    
    __tablename__ = "session"    
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, user_id):
        """Initializes the session for a user"""
        self.id = UUID(bytes = OpenSSL.rand.bytes(16)).hex
        self.user_id = user_id
