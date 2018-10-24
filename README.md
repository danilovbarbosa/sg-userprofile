# sg-userprofile
Service for common user profiling in serious games

## Create an environment (Linux)

mkdir myproject

cd myproject

python3 -m venv venv

## Activate the environment (First, remember to activate the virtualenv, if any)

. venv/bin/activate

## Try it out

Clone project (branch sg-userProfileDeaf):

git clone -b sg-userProfileDeaf https://github.com/danilovbarbosa/sg-userprofile.git

Install the requirements

pip install -r requirements.txt

Add file './gameevents/config.py' with configuration from: SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, WTF_CSRF_ENABLED, SECRET_KEY, SQLALCHEMY_DATABASE_URI_TEST, TMPDIR, LOG_FILENAME, LOG_FILENAME_TEST and DEFAULT_TOKEN_DURATION  
 
Then, create the database and the migration files:

$ python userprofile/db_create.py

$ python userprofile/db_migrate.py

Run the server

$ python userprofile/run.py

Add at least one username to the database:
** You can change tags: username and password.

$ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user", "password":"password"}' http://localhost:5002/v1/users

Request a sessionid:

$ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user","password":"password"}' http://localhost:5002/v1/sessions

See user data associated to a sessionid:
$ curl -i http://localhost:5002/v1/sessions/YOURSESSIONID
