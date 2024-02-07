import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.ticket.create import TicketCreateService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class CreateTicketHandler(ProtectedHandler):

    """
    Handles the creation of a new ticket.
    """

    required_fields = [
        'forensic_evidence'
    ]

    optional_fields = [
        'dda_id',
        'description',
        'fqdn',
        'ipv4',
        'ipv6',
        'assigned_to'
    ]

    async def post(self):
        """
        Handles the ticket creation.
        """

        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields, self.optional_fields) == False:
            return

        try:
            # verify permissions
            self.permission_service.can_create_ticket()

            ticket_create_service = TicketCreateService()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                ticket_id, revoke_time = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_create_service.execute,
                    self.request_data.get('dda_id'),
                    self.request_data.get('forensic_evidence'),
                    self.request_data.get('fqdn') or [],
                    self.request_data.get('ipv4') or [],
                    self.request_data.get('ipv6') or [],
                    self.request_data.get('assigned_to') or [],
                    self.account_data.get('account_id'),
                    self.request_data.get('description') or None
                )

                self.success(
                    data = { 'ticket_id': ticket_id },
                    note = f'Ticket created. If this is a mistake, you have {revoke_time} seconds to remove it before it gets visible to the providers.'
                )

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                ticket_id, revoke_time = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    ticket_create_service.execute,
                    self.request_data.get('dda_id'),
                    self.request_data.get('forensic_evidence'),
                    self.request_data.get('fqdn') or [],
                    self.request_data.get('ipv4') or [],
                    self.request_data.get('ipv6') or [],
                    self.request_data.get('assigned_to') or [], # TEMPORARY
                    #[], # currently, we do not allow any choice by the reporter to which provider will receive the ticket
                    self.account_data.get('account_id'),
                    self.request_data.get('description') or None
                )

                self.success(
                    data = { 'ticket_id': ticket_id },
                    note = f'Ticket created. If this is a mistake, you have {revoke_time} seconds to remove it before it gets visible to the providers.'
                )

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
