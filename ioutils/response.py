from tornado.web import RequestHandler

from piracyshield_component.config import Config

from .errors import ErrorCode, ErrorMessage

import json

class ResponseHandler(RequestHandler):

    """
    Response handler.

    Prepares the response parameters for the next layer (Request).
    """

    def set_default_headers(self) -> None:
        """
        Sets the default headers.
        """

        # allow CORS only from current domain
        self.set_header('Access-Control-Allow-Origin', self.application.domain)

        self.set_header('Access-Control-Allow-Methods', self.application.allowed_methods)

        self.set_header('Access-Control-Max-Age', self.application.max_age)

        # response for this API is always a JSON
        self.set_header('Content-Type', 'application/json')

        # sets the server name
        # TODO: let this be configurable
        self.set_header('Server', 'piracy-shield')

    def set_refresh_cookie(self, value: str) -> None:
        """
        Cookie setter.

        TODO: need to extend this and have these data loaded from the external config.

        :param key: name of the cookie.
        :param value: value of the cookie.
        """

        self.set_secure_cookie(
            name = 'refresh_token',
            value = value,
            expires_days = 1,
            httponly = True,
            samesite = "Strict",
            secure = True
        )

    def get_refresh_cookie(self) -> any:
        """
        Handy function to return the refresh token cookie.
        """

        return self.get_secure_cookie('refresh_token')

    def clear_cookie(self, key: str, **kwargs) -> None:
        """
        Cookie remover.

        :param key: name of the cookie.
        """

        # set to -365 days
        expires = -31536000

        self.set_cookie(key, value = '', expires = expires, **kwargs)

    def success_txt(self, data: str) -> None:
        """
        Returns a string in TXT.

        :param data: a string to send back as response.
        """

        self.set_header('Content-Type', 'text/plain; charset=UTF-8')

        self.set_status(200)

        self.finish(self.str_to_txt(data))

    def success_list_txt(self, data: list) -> None:
        """
        Returns a list in TXT.

        :param data: a list to send back as response.
        """

        self.set_header('Content-Type', 'text/plain; charset=UTF-8')

        self.set_status(200)

        self.finish(self.list_to_txt(data))

    def success(self, data = None, note = None) -> None:
        """
        Success response.

        :param data: returns data if needed.
        """

        self.set_status(200)

        response = {
            'status': 'success'
        }

        # ensures these data are appended in any case, even if empty
        if isinstance(data, str) or isinstance(data, list) or isinstance(data, dict):
            response['data'] = data

        # generic purpose informations that we want to communicate
        if note:
            response['note'] = note

        self.finish(self.to_json(response))

    def error(self, status_code: int, error_code: int, message: str) -> None:
        """
        Returns custom format error.

        :param status_code: HTTP status code.
        :param error_code: custom error code.
        :param message: reason of the error.
        """

        self.set_status(status_code)

        response = {
            'status': 'error',
            'code': error_code,
            'message': message
        }

        self.application.logger.debug(f'< ERR `{self.request.uri}` {status_code}')

        self.finish(self.to_json(response))

        # prevent further execution of the code
        self._handled = False

        # stop execution of the request
        self._finished = True

    def write_error(self, status_code, **kwargs) -> None:
        """
        Override the generic error handler.

        :param status_code: HTTP status code.
        """

        match status_code:
            case 403:
                self.error(
                    status_code = 403,
                    error_code = ErrorCode.FORBIDDEN,
                    message = ErrorMessage.FORBIDDEN
                )

            case 404:
                self.error(
                    status_code = 404,
                    error_code = ErrorCode.ROUTE_NOT_FOUND,
                    message = ErrorMessage.ROUTE_NOT_FOUND
                )

            case 405:
                self.error(
                    status_code = 405,
                    error_code = ErrorCode.METHOD_NOT_ALLOWED,
                    message = ErrorMessage.METHOD_NOT_ALLOWED
                )

            case _:
                self.error(
                    status_code = 400,
                    error_code = ErrorCode.GENERIC,
                    message = ErrorMessage.GENERIC
                )

    def to_json(self, response: dict) -> str:
        """
        Converts dictionary into a valid JSON string.

        :param response: response data.
        """

        return json.dumps(response)

    def str_to_txt(self, data: str) -> str:
        """
        Converts a list into an UTF-8 string of line by line elements.

        :param data: the data to convert.
        """

        if data:
            return data.encode('utf-8')

        return ''

    def list_to_txt(self, data: list) -> str:
        """
        Converts a list into an UTF-8 string of line by line elements.

        :param data: the data to convert.
        """

        if data:
            converted_data = '\n'.join(data)

            return converted_data.encode('utf-8')

        return ''
