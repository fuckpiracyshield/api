import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.dda.get_all_by_account import DDAGetAllByAccountService

from piracyshield_component.exception import ApplicationException

class GetAllDDAHandler(ProtectedHandler):

    """
    Handles getting multiple DDA identifiers.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            self.permission_service.can_view_dda()

            # check what level of view we have
            dda_get_all_by_account_service = DDAGetAllByAccountService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                dda_get_all_by_account_service.execute,
                self.account_data.get('account_id')
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
