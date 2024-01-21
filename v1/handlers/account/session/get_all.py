import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.permission.service import PermissionService
from piracyshield_service.account.session.get_all_by_account_ordered import AccountSessionGetAllByAccountOrderedService

from piracyshield_component.exception import ApplicationException

class GetAllSessionAccountHandler(ProtectedHandler):

    """
    Handles getting multiple active sessions.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            account_session_get_all_by_account_ordered_service = AccountSessionGetAllByAccountOrderedService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                account_session_get_all_by_account_ordered_service.execute,
                self.account_data.get('account_id'),
                self.current_access_token
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
