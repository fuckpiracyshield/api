import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.internal.change_password import InternalChangePasswordService

from piracyshield_component.exception import ApplicationException

class ChangePasswordInternalAccountHandler(ProtectedHandler):

    """
    Handles account password change.
    """

    required_fields = [
        'current_password',
        'new_password',
        'confirm_password'
    ]

    async def post(self):
        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            internal_account_change_password_service = InternalChangePasswordService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                internal_account_change_password_service.execute,
                self.account_data.get('account_id'),
                self.request_data.get('current_password'),
                self.request_data.get('new_password'),
                self.request_data.get('confirm_password')
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
