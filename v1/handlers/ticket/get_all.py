import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.get_all import TicketGetAllService
from piracyshield_service.ticket.get_all_by_reporter import TicketGetAllByReporterService
from piracyshield_service.ticket.get_all_by_provider import TicketGetAllByProviderService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetAllTicketHandler(ProtectedHandler):

    """
    Handles getting multiple tickets.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            # verify permissions
            self.permission_service.can_view_ticket()

            # check what level of view we have
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                ticket_get_all_service = TicketGetAllService()

                # we can get every kind of document
                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_all_service.execute
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_get_all_by_reporter_service = TicketGetAllByReporterService()

                # get only tickets created by that specific account
                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_all_by_reporter_service.execute,
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.PROVIDER.value:
                ticket_get_all_by_provider_service = TicketGetAllByProviderService()

                # get every ticket
                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_get_all_by_provider_service.execute,
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
