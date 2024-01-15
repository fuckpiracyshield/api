import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.internal.remove import InternalRemoveService

from piracyshield_component.exception import ApplicationException

class RemoveInternalAccountHandler(ProtectedHandler):

    """
    Handles the account removal.
    """

    required_fields = [
        'account_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_delete_account()

            internal_account_remove_service = InternalRemoveService()

            await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                internal_account_remove_service.execute,
                self.request_data.get('account_id')
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
