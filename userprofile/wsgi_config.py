import sys

path = '/home/carvalhomb/sg-userprofile/userprofile'
if path not in sys.path:
    sys.path.append(path)

from userprofile_app import create_app

application = create_app()