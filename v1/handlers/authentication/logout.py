import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ioutils.protected import ProtectedHandler

from piracyshield_component.exception import ApplicationException

class AuthenticationLogoutHandler(ProtectedHandler):

    """
    Removes the authentication refresh token.
    The effective logout remains on the access token expiration time, this is why it should be set to a short time.
    """

    def get(self):
        if self.initialize_account() == False:
            return

        self.clear_cookie('refresh_token')

        self.success(data = 'Goodbye!')
