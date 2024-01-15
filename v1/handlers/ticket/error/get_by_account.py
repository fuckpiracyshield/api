import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.error.get import TicketErrorGetService
from piracyshield_service.ticket.error.get_by_reporter import TicketErrorGetByReporterService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetByReporterTicketErrorHandler(ProtectedHandler):

    """
    Handles getting error ticket for reporter account.
    """

    required_fields = [
        'ticket_error_id'
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
                ticket_error_get_service = TicketErrorGetService()

                # we can get every kind of document
                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_error_get_service.execute,
                    self.request_data.get('ticket_error_id')
                )

                self.success(data = response)

            if self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_error_get_by_reporter = TicketErrorGetByReporterService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_error_get_by_reporter.execute,
                    self.request_data.get('ticket_error_id'),
                    self.account_data.get('account_id')
                )

                self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
