'''
Run the application
'''

import os
import sys

sys.path.append(os.path.dirname(__name__))

#from sample_application import create_app
from userprofile_app import create_app
from userprofile_app.models import Session, User

# create an app instance
app = create_app()

app.run(debug=True, port=5002)
