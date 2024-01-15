import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.get_total import TicketGetTotalService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetTotalTicketHandler(ProtectedHandler):

    """
    Handles getting all the tickets.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value or self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_get_total_service = TicketGetTotalService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_total_service.execute
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
