import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.ticket.item.set_processed import TicketItemSetProcessedService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class SetTicketItemProcessedHandler(ProtectedHandler):

    """
    Handles setting the processed status of a single ticket item.
    """

    required_fields = [
        'value'
    ]

    optional_fields = [
        'timestamp'
        'note'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields, self.optional_fields) == False:
            return

        try:
            self.permission_service.can_edit_ticket()

            if self.account_data.get('role') == AccountRoleModel.PROVIDER.value:
                ticket_item_set_processed_service = TicketItemSetProcessedService()

                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_item_set_processed_service.execute,
                    self.account_data.get('account_id'),
                    self.request_data.get('value'),
                    self.request_data.get('timestamp') or None,
                    self.request_data.get('note') or None
                )

                self.success()

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
