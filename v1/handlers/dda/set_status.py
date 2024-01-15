import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.dda.set_status import DDASetStatusService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class SetStatusActiveDDAHandler(ProtectedHandler):

    """
    Handles the status of a DDA identifier.
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
            self.permission_service.can_edit_dda()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                dda_set_status_service = DDASetStatusService()

                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    dda_set_status_service.execute,
                    self.request_data.get('dda_id'),
                    True
                )

                self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)

class SetStatusNonActiveDDAHandler(ProtectedHandler):

    """
    Handles the status of a DDA identifier.
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
            self.permission_service.can_edit_dda()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                dda_set_status_service = DDASetStatusService()

                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    dda_set_status_service.execute,
                    self.request_data.get('dda_id'),
                    False
                )

                self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
