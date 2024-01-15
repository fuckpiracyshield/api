import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.provider.remove import ProviderRemoveService

from piracyshield_component.exception import ApplicationException

class RemoveProviderAccountHandler(ProtectedHandler):

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
            # ensure that we have the proper permissions for this operation
            self.permission_service.can_delete_account()

            provider_account_remove_service = ProviderRemoveService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                provider_account_remove_service.execute,
                self.request_data.get('account_id')
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
