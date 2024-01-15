import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.permission.service import PermissionService
from piracyshield_service.account.general.get import GeneralAccountGetService

from piracyshield_component.exception import ApplicationException

class GetGeneralAccountHandler(ProtectedHandler):

    """
    Handles getting a single account by its account identifier.
    """

    required_fields = [
        'account_id'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            self.permission_service.can_view_account()

            general_account_get_service = GeneralAccountGetService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                general_account_get_service.execute,
                self.request_data.get('account_id')
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
