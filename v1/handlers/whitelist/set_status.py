import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.whitelist.set_status import WhitelistSetStatusService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class SetStatusActiveWhitelistItemHandler(ProtectedHandler):

    """
    Handles the status of a whitelist item.
    """

    required_fields = [
        'item'
    ]

    async def post(self):
        """
        Handles the whitelist item active status.
        """

        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_edit_whitelist_item()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                whitelist_set_status_service = WhitelistSetStatusService()

                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    whitelist_set_status_service.execute,
                    self.request_data.get('item'),
                    True
                )

                self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)

class SetStatusNonActiveWhitelistItemHandler(ProtectedHandler):

    """
    Handles the status of a whitelist item.
    """

    required_fields = [
        'item'
    ]

    async def post(self):
        """
        Handles the whitelist item non active status.
        """

        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_edit_whitelist_item()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                whitelist_set_status_service = WhitelistSetStatusService()

                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    whitelist_set_status_service.execute,
                    self.request_data.get('item'),
                    False
                )

                self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
