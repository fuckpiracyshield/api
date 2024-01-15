import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler

from piracyshield_service.internal.set_status import InternalSetStatusService

from piracyshield_component.exception import ApplicationException

class SetStatusActiveInternalAccountHandler(ProtectedHandler):

    """
    Handles account activation.
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
            self.permission_service.can_edit_account()

            internal_account_set_status_service = InternalSetStatusService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                internal_account_set_status_service.execute,
                self.request_data.get('account_id'),
                True
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)

class SetStatusNonActiveInternalAccountHandler(ProtectedHandler):

    """
    Handles account deactivation.
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
            self.permission_service.can_edit_account()

            internal_account_set_status_service = InternalSetStatusService()

            response = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                internal_account_set_status_service.execute,
                self.request_data.get('account_id'),
                False
            )

            self.success(data = response)

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
