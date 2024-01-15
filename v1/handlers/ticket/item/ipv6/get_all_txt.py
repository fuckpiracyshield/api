import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.item.ipv6.get_all import TicketItemIPv6GetAllService
from piracyshield_service.ticket.item.ipv6.get_all_by_provider import TicketItemIPv6GetAllByProviderService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetAllIPv6TXTHandler(ProtectedHandler):

    """
    Handles getting all IPv6 items.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            self.permission_service.can_view_ticket()

            # only internal and provider accounts should get this data
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                ticket_item_ipv6_get_all_service = TicketItemIPv6GetAllService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_ipv6_get_all_service.execute
                )

                self.success_list_txt(data = response)

            elif self.account_data.get('role') == AccountRoleModel.PROVIDER.value:
                ticket_item_ipv6_get_all_by_provider_service = TicketItemIPv6GetAllByProviderService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_ipv6_get_all_by_provider_service.execute,
                    self.account_data.get('account_id')
                )

                self.success_list_txt(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
