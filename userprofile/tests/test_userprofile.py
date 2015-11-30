'''
Unit tests for user profile module
'''
import unittest
#import time
#import datetime
import json
import sys
#from json.decoder import JSONDecodeError
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

    @classmethod
    def setUpClass(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        #Create a brand new test db
        db.create_all()
        
        LOG.info("Initializing tests.")
        
        new_user = User("admin", "adminpassword")
        db.session.add(new_user)
        
        new_normal_user = User("normaluser", "password")
        db.session.add(new_normal_user)
        
        new_normal_user2 = User("normaluser2", "password")
        db.session.add(new_normal_user2)
        
        try:
            db.session.commit()
        except Exception as e:
            LOG.error(e, exc_info=True)
        
        new_session = Session(new_normal_user)
        self.mysessionid = new_session.id
        db.session.add(new_session)
        
        try:
            db.session.commit()
        except Exception as e:
            LOG.error(e, exc_info=True)
        
        new_session_todelete = Session(new_normal_user2)
        self.mysessionid_todelete = new_session_todelete.id
        db.session.add(new_session_todelete)

    @classmethod
    def tearDownClass(self):
        LOG.info("======================Finished tests====================")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
        
        
        
###################################################
#    User-related tests
###################################################


    def test_add_user(self):
        requestdata = json.dumps(dict(username="normaluser3", password="123456"))
        response = self.client.post('/userprofile/api/v1.0/users', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "201 CREATED")
        
    def test_add_user_bad_request(self):
        requestdata = json.dumps(dict(username="normaluser3"))
        response = self.client.post('/userprofile/api/v1.0/users', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "400 BAD REQUEST")
    
    def test_add_user_empty_values(self):
        requestdata = json.dumps(dict(username="", password=""))
        response = self.client.post('/userprofile/api/v1.0/users', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "400 BAD REQUEST")
    
    def test_add_repeated_user(self):
        requestdata = json.dumps(dict(username="admin", password="123456"))
        response = self.client.post('/userprofile/api/v1.0/users', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "409 CONFLICT")
        
    
    
###################################################
#    Session-related tests
###################################################
    
    def test_request_sessionid_good_credentials(self):
        requestdata = json.dumps(dict(username="normaluser", password="password"))
        response = self.client.post('/userprofile/api/v1.0/sessions', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        json_results = json.loads(response.get_data().decode())
        self.assertEquals(response.status, "200 OK")
        LOG.debug("Returned sessionid: %s" % json_results["sessionid"])
        
    def test_request_sessionid_bad_credentials(self):
        requestdata = json.dumps(dict(username="wrongnormaluser", password="wrongpassword"))
        response = self.client.post('/userprofile/api/v1.0/sessions', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        #json_results = json.loads(response.get_data().decode())
        self.assertEquals(response.status, "401 UNAUTHORIZED")
        
    def test_request_sessionid_bad_password(self):
        requestdata = json.dumps(dict(username="normaluser", password="wrongpassword"))
        response = self.client.post('/userprofile/api/v1.0/sessions', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        #json_results = json.loads(response.get_data().decode())
        self.assertEquals(response.status, "401 UNAUTHORIZED")

    def test_request_sessionid_bad_request(self):
        requestdata = json.dumps(dict(username="normaluser"))
        response = self.client.post('/userprofile/api/v1.0/sessions', 
                                 data=requestdata, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        #json_results = json.loads(response.get_data().decode())
        self.assertEquals(response.status, "400 BAD REQUEST")
        
    def test_request_sessionid_wrong_method(self):
        response = self.client.get('/userprofile/api/v1.0/sessions', 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")
        
    def test_delete_sessionid(self):
        response = self.client.delete('/userprofile/api/v1.0/sessions/%s' % self.mysessionid_todelete, 
                                 content_type = 'application/json', 
                                 follow_redirects=True)
        self.assertEquals(response.status, "200 OK")
        
###################################################
#    Get info from session - tests
###################################################

    def test_request_user_info_from_sessionid(self):
        #requestdata = json.dumps(dict(sessionid=self.mysessionid))
        response = self.client.get('/userprofile/api/v1.0/sessions/%s' % self.mysessionid, 
                                 #data=requestdata, 
                                 #content_type = 'application/json', 
                                 follow_redirects=True)
        try:
            json_results = json.loads(response.get_data().decode())
        except ValueError:
            self.fail("Not a JSON response, something went wrong.")
        self.assertEquals(response.status, "200 OK")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()