import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.internal.get import InternalGetService

from piracyshield_component.exception import ApplicationException

class GetInternalAccountHandler(ProtectedHandler):

    """
    Handles getting a single account by its ID.
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
            self.permission_service.can_view_account()

            internal_account_get_service = InternalGetService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                internal_account_get_service.execute,
                self.request_data.get('account_id')
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
