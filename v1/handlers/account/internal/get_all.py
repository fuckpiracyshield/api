import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.internal.get_all import InternalGetAllService

from piracyshield_component.exception import ApplicationException

class GetAllInternalAccountHandler(ProtectedHandler):

    """
    Handles getting multiple accounts.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            self.permission_service.can_view_account()

            internal_account_get_all_service = InternalGetAllService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                internal_account_get_all_service.execute
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
