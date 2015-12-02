'''
Creates a few custom exceptions used throughout the application.
'''

class UsernameExistsException(Exception):
    '''
    Username already exists in database.
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class SessionidNotFoundException(Exception):
    '''
    Session ID not found in database.
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class UserNotFoundException(Exception):
    '''
    User not found in database.
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)