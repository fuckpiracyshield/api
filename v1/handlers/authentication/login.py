import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.base import BaseHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.authentication.authenticate import AuthenticationAuthenticateService
from piracyshield_service.authentication.generate_access_token import AuthenticationGenerateAccessTokenService
from piracyshield_service.authentication.generate_refresh_token import AuthenticationGenerateRefreshTokenService

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
            access_token, refresh_token = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                self.process,
                self.request_data.get('email'),
                self.request_data.get('password'),
                self.request.remote_ip
            )

            self.success(data = {
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)

    def process(self, email: str, password: str, ip_address: str) -> tuple:
        authentication_authenticate_service = AuthenticationAuthenticateService()

        # try to authenticate
        payload = authentication_authenticate_service.execute(
            email = email,
            password = password,
            ip_address = ip_address
        )

        authentication_generate_access_token_service = AuthenticationGenerateAccessTokenService()
        authentication_generate_refresh_token_service = AuthenticationGenerateRefreshTokenService()

        # generate token pairs
        access_token = authentication_generate_access_token_service.execute(payload)
        refresh_token = authentication_generate_refresh_token_service.execute(payload)

        # store the refresh_token in a http-only cookie
        self.set_refresh_cookie(value = refresh_token)

        return access_token, refresh_token
