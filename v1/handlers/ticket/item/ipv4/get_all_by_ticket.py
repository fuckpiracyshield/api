import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.item.ipv4.get_all_by_ticket import TicketItemIPv4GetAllByTicketService
from piracyshield_service.ticket.item.ipv4.get_all_by_ticket_for_reporter import TicketItemIPv4GetAllByTicketForReporterService
from piracyshield_service.ticket.item.ipv4.get_all_by_ticket_for_provider import TicketItemIPv4GetAllByTicketForProviderService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetTicketIPv4Handler(ProtectedHandler):

    """
    Handles getting all IPv4 items for a ticket.
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
            self.permission_service.can_view_ticket()

            # only internal and provider accounts should get this data
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                ticket_item_ipv4_get_all_by_ticket_service = TicketItemIPv4GetAllByTicketService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_ipv4_get_all_by_ticket_service.execute,
                    self.request_data.get('ticket_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_item_ipv4_get_all_by_ticket_for_reporter_service = TicketItemIPv4GetAllByTicketForReporterService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_ipv4_get_all_by_ticket_for_reporter_service.execute,
                    self.request_data.get('ticket_id'),
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.PROVIDER.value:
                ticket_item_ipv4_get_all_by_ticket_for_provider_service = TicketItemIPv4GetAllByTicketForProviderService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_ipv4_get_all_by_ticket_for_provider_service.execute,
                    self.request_data.get('ticket_id'),
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
