from .base import BaseHandler

from piracyshield_component.exception import ApplicationException

from piracyshield_service.authentication.verify_access_token import AuthenticationVerifyAccessTokenService

from piracyshield_service.permission.service import PermissionService

from piracyshield_data_model.account.role.model import AccountRoleModel

from .errors import ErrorCode, ErrorMessage

class ProtectedHandler(BaseHandler):

    """
    Restricts access to authenticated users only.
    """

    bypassed_routes = [
        '/change_password',
        '/logout'
    ]

    authentication_verify_access_token_service = None

    permission_service = None

    account_data = {}

    def prepare(self):
        self.authentication_verify_access_token_service = AuthenticationVerifyAccessTokenService()

        super().prepare()

    def initialize_account(self):
        """
        Performs the checks required to verify the JWT token and set up the account services.
        """

        authorization_header = self.request.headers.get('Authorization')

        # no token is passed
        if authorization_header is None:
            self.error(status_code = 401, error_code = ErrorCode.MISSING_TOKEN, message = ErrorMessage.MISSING_TOKEN)

            return False

        # we get something but not what we're looking for
        if not authorization_header.startswith('Bearer '):
            self.error(status_code = 401, error_code = ErrorCode.TOKEN_FORMAT_NON_VALID, message = ErrorMessage.TOKEN_FORMAT_NON_VALID)

            return False

        # get the token only
        token = authorization_header[7:]

        try:
            # set the current account data
            # TODO: absolutely need to validate the payload.
            self.account_data = self.authentication_verify_access_token_service.execute(token)

            if not self.account_data.get('email'):
                self.error(status_code = 401, error_code = ErrorCode.TOKEN_FORMAT_NON_VALID, message = ErrorMessage.TOKEN_FORMAT_NON_VALID)

                return False

            # verify account role
            try:
                AccountRoleModel(self.account_data.get('role'))

            except ValueError:
                self.error(status_code = 401, error_code = ErrorCode.TOKEN_FORMAT_NON_VALID, message = ErrorMessage.TOKEN_FORMAT_NON_VALID)

                return False

            # prevent application access if there's a mandatory password change
            if self.account_data.get('flags').get('change_password') == True:
                # hacky way to prevent useful routes from being filtered as well
                if not any(path in self.request.path for path in self.bypassed_routes):
                #if 'change_password' not in self.request.path:
                    self.error(status_code = 401, error_code = ErrorCode.CHANGE_PASSWORD, message = ErrorMessage.CHANGE_PASSWORD)

                    return False

            # initialize permission service
            self.permission_service = PermissionService(self.account_data.get('role'))

        except ApplicationException as e:
            self.error(status_code = 401, error_code = e.code, message = e.message)

            return False

        return True
