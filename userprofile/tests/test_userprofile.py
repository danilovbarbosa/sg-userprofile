'''
Unit tests for user profile module
'''
import unittest
#import time
#import datetime
import json
import sys
#import base64
#from werkzeug.wrappers import Response
sys.path.append("..") 

#from flask import current_app

#from werkzeug.datastructures import Headers

from userprofile_app import create_app

#Extensions
from userprofile_app.extensions import db, LOG


from userprofile_app.models import User,Session

class TestUserProfile(unittest.TestCase):


    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        #Create a brand new test db
        db.create_all()
        
        LOG.info("Initializing tests.")
        
        new_user = User("admin", "adminpassword")
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
        
        


    def tearDown(self):
        LOG.info("======================Finished tests====================")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_add_user(self):
        requestdata = json.dumps(dict(username="normaluser", password="123456"))
        response = self.client.post('/userprofile/api/v1.0/user', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "201 CREATED")
        
    def test_add_user_bad_request(self):
        requestdata = json.dumps(dict(username="normaluser"))
        response = self.client.post('/userprofile/api/v1.0/user', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "400 BAD REQUEST")
    
    def test_add_user_empty_values(self):
        requestdata = json.dumps(dict(username="", password=""))
        response = self.client.post('/userprofile/api/v1.0/user', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "400 BAD REQUEST")
    
    def test_add_repeated_user(self):
        requestdata = json.dumps(dict(username="admin", password="123456"))
        response = self.client.post('/userprofile/api/v1.0/user', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "409 CONFLICT")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()