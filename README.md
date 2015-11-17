# sg-userprofile
Service for common user profiling in serious games

## Try it out

First, remember to activate the virtualenv, if any
 
Then, create the database and the migration files:

$ python userprofile/db_create.py
$ python userprofile/db_migrate.py

Run the server

$ python userprofile/run.py

Add at least one username to the database:

$ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user", "password":"password"}' http://localhost:5002/userprofile/api/v1.0/users

Request a sessionid:

$ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user","password":"password"}' http://localhost:5002/userprofile/api/v1.0/sessions

See user data associated to a sessionid:
$ curl -i http://localhost:5002/userprofile/api/v1.0/sessions/YOURSESSIONID