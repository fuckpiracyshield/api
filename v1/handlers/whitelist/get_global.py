import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.whitelist.get_global import WhitelistGetGlobalService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetGlobalWhitelistItemHandler(ProtectedHandler):

    """
    Handles getting multiple whitelist items.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            self.permission_service.can_view_whitelist_item()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                # check what level of view we have
                whitelist_get_global_service = WhitelistGetGlobalService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    whitelist_get_global_service.execute
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
