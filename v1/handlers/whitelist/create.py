import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.whitelist.create import WhitelistCreateService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class CreateWhitelistItemHandler(ProtectedHandler):

    """
    Handles the creation of a new whitelist item.
    """

    required_fields = [
        'genre',
        'item'
    ]

    optional_fields = [
        'registrar',
        'as_code'
    ]

    async def post(self):
        """
        Handles the whitelist item creation.
        """

        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields, self.optional_fields) == False:
            return

        try:
            self.permission_service.can_create_whitelist_item()

            whitelist_create_service = WhitelistCreateService()

            await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                whitelist_create_service.execute,
                self.request_data.get('genre'),
                self.request_data.get('item'),
                self.account_data.get('account_id'),
                self.request_data.get('registrar') or None,
                self.request_data.get('as_code') or None
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
