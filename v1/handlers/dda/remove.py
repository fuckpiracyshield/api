import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.dda.remove import DDARemoveService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class RemoveDDAHandler(ProtectedHandler):

    """
    Handles the DDA identifier removal.
    """

    required_fields = [
        'dda_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_delete_dda()

            dda_remove_service = DDARemoveService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                dda_remove_service.execute,
                self.request_data.get('dda_id')
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
