import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.whitelist.remove import WhitelistRemoveService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class RemoveWhitelistItemHandler(ProtectedHandler):

    """
    Handles the whitelist item removal.
    """

    required_fields = [
        'item'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_delete_whitelist_item()

            whitelist_remove_service = WhitelistRemoveService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                whitelist_remove_service.execute,
                self.request_data.get('item'),
                self.account_data.get('account_id')
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
