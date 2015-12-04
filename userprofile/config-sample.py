import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Flask stuff
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI = "mysql://userprofile:userprofile@localhost/userprofile"
WTF_CSRF_ENABLED = False
SECRET_KEY = 'heytheredonottrytomesswithmemister3'

#Other config
SQLALCHEMY_DATABASE_URI_TEST = "mysql://userprofile:userprofile@localhost/userprofile_test"
TMPDIR = os.path.join(basedir, '..', 'tmp')
LOG_FILENAME = "userprofile.log.txt"
LOG_FILENAME_TEST = "userprofile_testing.log.txt"

DEFAULT_TOKEN_DURATION = 600 #IN SECONDS
