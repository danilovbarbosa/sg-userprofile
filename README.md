# sg-userprofile
Service for common user profiling in serious games that realize comunication with service [sg-gameevents](https://github.com/danilovbarbosa/sg-gameevents/tree/sg-eventsGameDeaf).

## Create an environment (Linux)
``` 
$ mkdir myproject

$ cd myproject 

$ python3 -m venv venv 
```

## Activate the environment (First, remember to activate the virtualenv, if any)

``` $ . venv/bin/activate ```

## Try it out

### Clone project (branch sg-userProfileDeaf):

```  git clone -b sg-userProfileDeaf https://github.com/danilovbarbosa/sg-userprofile.git ``` 

### Install the requirements

``` $ pip install -r requirements.txt ```

> Add file './gameevents/config.py' with configuration from: SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, WTF_CSRF_ENABLED, SECRET_KEY, SQLALCHEMY_DATABASE_URI_TEST, TMPDIR, LOG_FILENAME, LOG_FILENAME_TEST and DEFAULT_TOKEN_DURATION  
 
### Then, create the database and the migration files:

> Remember, before you run the commands, you should create schemas in database MySql: userprofile and userprofile_test

```
$ python gameevents/db_create.py

$ python gameevents/db_migrate.py 
```

### Run the server:

``` $ python gameevents/run.py ```

> Add at least one username to the database: you can change tags: username and password.

```  $ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user", "password":"password"}' http://localhost:5002/v1/users ``` 

### Request a sessionid:

```  $ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user","password":"password"}' http://localhost:5002/v1/sessions ``` 

### See user data associated to a sessionid:
``` $ curl -i http://localhost:5002/v1/sessions/YOURSESSIONID ``` 
