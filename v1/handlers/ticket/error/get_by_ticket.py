import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.error.get_by_ticket import TicketErrorGetByTicketService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetByTicketTicketErrorHandler(ProtectedHandler):

    """
    Handles getting multiple error tickets.
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
            self.permission_service.can_view_ticket()

            # check what level of view we have
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                ticket_error_get_by_ticket = TicketErrorGetByTicketService()

                # we can get every kind of document
                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_error_get_by_ticket.execute,
                    self.request_data.get('ticket_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_error_get_by_ticket = TicketErrorGetByTicketService()

                # get only tickets created by that specific account
                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_error_get_by_ticket.execute,
                    self.request_data.get('ticket_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
