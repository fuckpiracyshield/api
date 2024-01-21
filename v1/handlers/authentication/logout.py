import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ioutils.protected import ProtectedHandler

from piracyshield_service.account.session.destroy_current_sessions import AccountSessionDestroyCurrentSessionsService

from piracyshield_component.exception import ApplicationException

class AuthenticationLogoutHandler(ProtectedHandler):

    """
    Removes the authentication refresh token and blacklists both the tokens.
    """

    def get(self):
        if self.initialize_account() == False:
            return

        try:
            account_session_destroy_current_sessions_service = AccountSessionDestroyCurrentSessionsService()

            account_session_destroy_current_sessions_service.execute(
                self.account_data.get('account_id'),
                self.current_access_token
            )

            self.clear_cookie('refresh_token')

            self.success(data = 'Goodbye!')

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
