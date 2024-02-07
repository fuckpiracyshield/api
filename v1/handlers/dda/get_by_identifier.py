import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.dda.get_by_identifier import DDAGetByIdentifierService
from piracyshield_service.dda.get_by_identifier_for_reporter import DDAGetByIdentifierForReporterService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetByIdentifierDDAHandler(ProtectedHandler):

    """
    Handles getting a single DDA by its identifier.
    """

    required_fields = [
        'dda_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            # check what level of view we have
            if self.account_data.get('role') == AccountRoleModel.INTERNAL.value:
                dda_get_by_identifier_service = DDAGetByIdentifierService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    dda_get_by_identifier_service.execute,
                    self.request_data.get('dda_id')
                )

                self.success(data = response)

            elif self.account_data.get('role') == AccountRoleModel.REPORTER.value:
                dda_get_by_identifier_for_reporter_service = DDAGetByIdentifierForReporterService()

                response = await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    dda_get_by_identifier_for_reporter_service.execute,
                    self.request_data.get('dda_id'),
                    self.account_data.get('account_id')
                )

                self.success(data = response)

            else:
                self.error(status_code = 403, error_code = ErrorCode.PERMISSION_DENIED, message = ErrorMessage.PERMISSION_DENIED)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
