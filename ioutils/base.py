from .request import RequestHandler

from .parameters import JSONParametersHandler, JSONParametersNonValidException, JSONParametersMissingException, JSONParametersTooManyException

from .errors import ErrorCode, ErrorMessage

class BaseHandler(RequestHandler):

    """
    Base class for initial input sanitizing and management.
    """

    request_data = {}

    def handle_post(self, required_fields: list, optional_fields: list = None, sanitization_rules: list = None) -> None | Exception:
        """
        Handle POST parameters.

        :param required_fields: a list of mandatory fields.
        :param optional_fields: a list of non-mandatory fields.
        :param sanitization_rules: a list of rules based on the Filter class component.
        """

        request_body = self.request.body.decode('utf-8')

        try:
            json_handler = JSONParametersHandler(request_body)

            # will raise an exception if the content is not what we're expecting
            processed_request = json_handler.process_request(
                required_fields = required_fields,
                optional_fields = optional_fields,
                sanitization_rules = sanitization_rules
            )

            self.request_data = {}

            # save the processed parameters so we can access them from child classes
            for key, value in processed_request.items():
                self.request_data[key] = value

        except JSONParametersNonValidException:
            self.error(status_code = 400, error_code = ErrorCode.NON_VALID_PARAMETERS, message = ErrorMessage.NON_VALID_PARAMETERS)

            return False

        except JSONParametersMissingException:
            self.error(status_code = 400, error_code = ErrorCode.MISSING_PARAMETERS, message = ErrorMessage.MISSING_PARAMETERS)

            return False

        except JSONParametersTooManyException:
            self.error(status_code = 400, error_code = ErrorCode.TOO_MANY_PARAMETERS, message = ErrorMessage.TOO_MANY_PARAMETERS)

            return False
