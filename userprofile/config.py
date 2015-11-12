'''
Created on 14 Oct 2015

@author: mbrandaoca
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Flask stuff
SQLITE_DB = 'userprofile.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, SQLITE_DB)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'heytheredonottrytomesswithmemister3'

#Other config
SQLITE_DB_TEST = 'userprofile_testing.db'
SQLALCHEMY_DATABASE_URI_TEST = 'sqlite:///' + os.path.join(basedir, SQLITE_DB_TEST)
TMPDIR = os.path.join(basedir, 'tmp')
LOG_FILENAME = "userprofile.log.txt"
LOG_FILENAME_TEST = "userprofile_testing.log.txt"

DEFAULT_TOKEN_DURATION = 600 #IN SECONDS