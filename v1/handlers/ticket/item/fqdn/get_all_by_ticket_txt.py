import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.item.fqdn.get_all_by_ticket import TicketItemFQDNGetAllByTicketService
from piracyshield_service.ticket.item.fqdn.get_all_by_ticket_for_provider import TicketItemFQDNGetAllByTicketForProviderService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetTicketFQDNTXTHandler(ProtectedHandler):

    """
    Handles getting all FQDN items for a ticket in a TXT.
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
                ticket_item_fqdn_get_all_by_ticket_service = TicketItemFQDNGetAllByTicketService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_fqdn_get_all_by_ticket_service.execute,
                    self.request_data.get('ticket_id')
                )

                self.success_list_txt(data = response)

            elif self.account_data.get('role') == AccountRoleModel.PROVIDER.value:
                ticket_item_fqdn_get_all_by_ticket_for_provider_service = TicketItemFQDNGetAllByTicketForProviderService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_fqdn_get_all_by_ticket_for_provider_service.execute,
                    self.request_data.get('ticket_id'),
                    self.account_data.get('account_id')
                )

                self.success_list_txt(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
