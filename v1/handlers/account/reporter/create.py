import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.reporter.create import ReporterCreateService

from piracyshield_component.exception import ApplicationException

class CreateReporterAccountHandler(ProtectedHandler):

    """
    Handles the creation of a new account.
    """

    required_fields = [
        'name',
        'email',
        'password',
        'confirm_password',
        'flags'
    ]

    async def post(self):
        """
        Handles the account creation.
        """

        if self.initialize_account() == False:
            return

        if self.handle_post(self.required_fields) == False:
            return

        try:
            # ensure that we have the proper permissions for this operation
            self.permission_service.can_create_account()

            reporter_account_create_service = ReporterCreateService()

            account_id = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                reporter_account_create_service.execute,
                self.request_data.get('name'),
                self.request_data.get('email'),
                self.request_data.get('password'),
                self.request_data.get('confirm_password'),
                self.request_data.get('flags'),
                self.account_data.get('account_id')
            )

            self.success(data = {
                'account_id': account_id
            })

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
