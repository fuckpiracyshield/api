import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.dda.create import DDACreateService

from piracyshield_component.exception import ApplicationException

class CreateDDAHandler(ProtectedHandler):

    """
    Handles the creation of a new DDA instance.
    """

    required_fields = [
        'description',
        'instance',
        'account_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_create_dda()

            dda_create_service = DDACreateService()

            await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                dda_create_service.execute,
                self.request_data.get('description'),
                self.request_data.get('instance'),
                self.request_data.get('account_id'),
                self.account_data.get('account_id')
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
