import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.forensic.get_by_ticket import ForensicGetByTicketService
from piracyshield_service.forensic.get_by_ticket_for_reporter import ForensicGetByTicketForReporterService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetByTicketForensicHandler(ProtectedHandler):

    """
    Handles the available forensic evidence by ticket identifier.
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
            self.permission_service.can_upload_ticket()

            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                forensic_get_by_ticket_service = ForensicGetByTicketService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    forensic_get_by_ticket_service.execute,
                    self.request_data.get('ticket_id')
                )

                self.success(
                    data = response
                )

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                forensic_get_by_ticket_for_reporter_service = ForensicGetByTicketForReporterService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    forensic_get_by_ticket_for_reporter_service.execute,
                    self.request_data.get('ticket_id'),
                    self.account_data.get('account_id')
                )

                self.success(
                    data = response
                )

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
