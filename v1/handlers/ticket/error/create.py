import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.ticket.error.create import TicketErrorCreateService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class CreateTicketErrorHandler(ProtectedHandler):

    """
    Handles the creation of a new error ticket.
    """

    required_fields = [
        'ticket_id'
    ]

    optional_fields = [
        'fqdn',
        'ipv4',
        'ipv6'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields, self.optional_fields) == False:
            return

        try:
            # verify permissions
            self.permission_service.can_create_ticket()

            ticket_error_create_service = TicketErrorCreateService()

            ticket_error_id, ticket_id = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                ticket_error_create_service.execute,
                self.request_data.get('ticket_id'),
                self.request_data.get('fqdn') or [],
                self.request_data.get('ipv4') or [],
                self.request_data.get('ipv6') or [],
                self.account_data.get('account_id')
            )

            self.success(data = {
                'ticket_error_id': ticket_error_id,
                'ticket_id': ticket_id
            })

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
