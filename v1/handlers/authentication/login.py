import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.base import BaseHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.authentication.authenticate import AuthenticationAuthenticateService

from piracyshield_component.exception import ApplicationException

class AuthenticationLoginHandler(BaseHandler):

    """
    Handles the account authentication.
    """

    required_fields = [
        'email',
        'password'
    ]

    async def post(self):
        """
        Handles the account authentication.
        """

        if self.handle_post(self.required_fields) == False:
            return

        try:
            authentication_authenticate_service = AuthenticationAuthenticateService()

            access_token, refresh_token = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                authentication_authenticate_service.execute,
                self.request_data.get('email'),
                self.request_data.get('password'),
                self.request.remote_ip
            )

            # store the refresh token in a http-only secure cookie
            self.set_refresh_cookie(value = refresh_token)

            self.success(data = {
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
