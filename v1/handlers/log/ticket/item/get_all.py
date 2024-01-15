import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.log.ticket.item.get_all import LogTicketItemGetAllService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetAllTicketItemLogHandler(ProtectedHandler):

    """
    Handles getting all the logs for a specific ticket item identifier.
    """

    required_fields = [
        'ticket_item_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                log_ticket_item_get_all_service = LogTicketItemGetAllService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    log_ticket_item_get_all_service.execute,
                    self.request_data.get('ticket_item_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
