import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.dda.get_all_by_account import DDAGetAllByAccountService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetAllByAccountDDAHandler(ProtectedHandler):

    """
    Handles getting multiple DDA identifiers by account.
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
            self.permission_service.can_view_dda()

            # check what level of view we have
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                dda_get_all_by_account_service = DDAGetAllByAccountService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    dda_get_all_by_account_service.execute,
                    self.request_data.get('account_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
