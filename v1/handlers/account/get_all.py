import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.permission.service import PermissionService
from piracyshield_service.account.general.get_all import GeneralAccountGetAllService

from piracyshield_component.exception import ApplicationException

class GetAllGeneralAccountHandler(ProtectedHandler):

    """
    Handles getting multiple accounts.
    """

    async def get(self):
        if self.initialize_account() == False:
            return

        try:
            self.permission_service.can_view_account()

            general_account_get_all_service = GeneralAccountGetAllService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                general_account_get_all_service.execute
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
