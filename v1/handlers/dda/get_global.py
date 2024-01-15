import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_service.dda.get_global import DDAGetGlobalService

from piracyshield_component.exception import ApplicationException

class GetGlobalDDAHandler(ProtectedHandler):

    """
    Handles getting multiple DDA identifiers.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            self.permission_service.can_view_dda()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                dda_get_global_service = DDAGetGlobalService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    dda_get_global_service.execute
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
