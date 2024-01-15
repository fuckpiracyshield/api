import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.get import TicketGetService
from piracyshield_service.ticket.get_by_reporter import TicketGetByReporterService
from piracyshield_service.ticket.get_by_provider import TicketGetByProviderService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetTicketHandler(ProtectedHandler):

    """
    Handles getting a single ticket by its ID.
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
                ticket_get_service = TicketGetService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_service.execute,
                    self.request_data.get('ticket_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_get_by_reporter_service = TicketGetByReporterService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_by_reporter_service.execute,
                    self.request_data.get('ticket_id'),
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.PROVIDER.value:
                ticket_get_by_provider_service = TicketGetByProviderService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_by_provider_service.execute,
                    self.request_data.get('ticket_id'),
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
