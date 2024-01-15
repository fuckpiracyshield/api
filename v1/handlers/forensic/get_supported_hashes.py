import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.forensic.get_supported_hashes import ForensicGetSupportedHashesService

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_component.exception import ApplicationException

class GetSupportedHashesForensicHandler(ProtectedHandler):

    """
    Handles the available hashes of a forensic evidence.
    """

    async def get(self):
        """
        Get the list of hashes available.
        """

        if self.initialize_account() == False:
            return

        try:
            # verify permissions
            self.permission_service.can_upload_ticket()

            forensic_get_supported_hashes_service = ForensicGetSupportedHashesService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                forensic_get_supported_hashes_service.execute
            )

            self.success(
                data = response
            )

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
