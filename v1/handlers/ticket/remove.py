import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.ticket.remove import TicketRemoveService

from piracyshield_data_model.account.role.model import AccountRoleModel
from piracyshield_data_model.ticket.status.model import TicketStatusModel

from piracyshield_component.exception import ApplicationException

class RemoveTicketHandler(ProtectedHandler):

    """
    Handles the ticket removal.
    """

    required_fields = [
        'ticket_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            # verify permissions
            self.permission_service.can_delete_ticket()

            ticket_remove_service = TicketRemoveService()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_remove_service.execute,
                    self.request_data.get('ticket_id')
                )

                self.success()

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_remove_service.execute,
                    self.request_data.get('ticket_id')
                )

                self.success()

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
