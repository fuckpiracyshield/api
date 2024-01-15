import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.base import BaseHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.authentication.verify_refresh_token import AuthenticationVerifyRefreshTokenService
from piracyshield_service.authentication.generate_access_token import AuthenticationGenerateAccessTokenService

from piracyshield_component.exception import ApplicationException

class AuthenticationRefreshHandler(BaseHandler):

    """
    Get another JWT access token once the main has expired.
    """

    optional_fields = [
        'refresh_token'
    ]

    async def post(self):
        # use stored refresh token when available
        refresh_token = self.get_refresh_cookie()

        # if no cookie available, generate a new access_token via POSTed refresh_token
        if not refresh_token:
            # if no refresh_token is found, we have an error
            if self.handle_post(required_fields = None, optional_fields = self.optional_fields) == False:
                return

            if not self.request_data.get('refresh_token'):
                return self.error(status_code = 403, error_code = ErrorCode.MISSING_REFRESH_TOKEN, message = ErrorMessage.MISSING_REFRESH_TOKEN)

            refresh_token = self.request_data.get('refresh_token')

        try:
            access_token = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                self.process,
                refresh_token
            )

            # return the access_token
            self.success(data = {
                'access_token': access_token
            })

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)

    def process(self, refresh_token: str) -> str:
        authentication_verify_refresh_token_service = AuthenticationVerifyRefreshTokenService()

        # verify the token and unwrap the payload
        payload = authentication_verify_refresh_token_service.execute(
            token = refresh_token
        )

        authentication_generate_access_token_service = AuthenticationGenerateAccessTokenService()

        # generate a new access token
        access_token = authentication_generate_access_token_service.execute(payload)

        return access_token
