from piracyshield_component.security.filter import Filter

import json

class JSONParametersHandler:

    """
    Pre-handle for the JSON request.
    """

    request_body = {}

    default_sanitization_rules = {
        'string': [
            'strip'
        ]
    }

    def __init__(self, request_body):
        self.request_body = request_body

    def process_request(self, required_fields: list = None, optional_fields: list = None, sanitization_rules: list = None) -> dict:
        """
        Validates and sanitizes incoming JSON request data.

        # TODO: need to determine a sanitization template for the rules as this is still a generic approach.

        :param required_fields: list of required fields.
        :param optional_fields: list of non-mandatory fields.
        :param sanitization_rules: list of required sanitizations.
        """

        # try to load the JSON data, this will raise an exception if the content is not valid
        try:
            self.request_body = json.loads(self.request_body)

        except Exception:
            raise JSONParametersNonValidException()

        if required_fields:
            self._validate_input(required_fields, optional_fields)

        if sanitization_rules:
            self.request_body = self._sanitize_input(self.request_body, sanitization_rules)

        else:
            self.request_body = self._sanitize_input(self.request_body, self.default_sanitization_rules)

        return self.request_body

    def _validate_input(self, required_fields: list, optional_fields: list) -> None | Exception:
        """
        Validates that the incoming JSON request contains all required fields.

        :param required_fields: list of required fields.
        :param optional_fields: list of non-mandatory fields.
        """

        if not optional_fields:
            # if there's no optional field we want the exact number of parameters
            if len(self.request_body) > len(required_fields):
                raise JSONParametersTooManyException()

        missing_fields = []

        for field in required_fields:
            if field not in self.request_body:
                missing_fields.append(field)

        if missing_fields:
            raise JSONParametersMissingException()

        # TODO: should we report the missing fields back to the user?

        return None

    def _sanitize_input(self, data: any, sanitization_rules: list) -> any:
        """
        Cleans the input data.

        :param data: any parameter in the request.
        :param sanitization_rules: list of cleaning rules.
        :return: the cleaned data.
        """

        if isinstance(data, dict):
            sanitized_data = {}

            for key, value in data.items():
                sanitized_value = self._sanitize_input(value, sanitization_rules)

                sanitized_data[key] = sanitized_value

            return sanitized_data

        elif isinstance(data, list):
            sanitized_data = []

            for item in data:
                sanitized_value = self._sanitize_input(item, sanitization_rules)

                if item:
                    sanitized_data.append(sanitized_value)

            return sanitized_data

        elif isinstance(data, str):
            if 'string' in sanitization_rules.keys():
                if 'strip' in sanitization_rules['string']:
                    return Filter.strip(data)

        else:
            return data

class JSONParametersNonValidException(Exception):

    """
    Not JSON data.
    """

    pass

class JSONParametersMissingException(Exception):

    """
    The parameters we're looking for are completely missing.
    """

    pass

class JSONParametersTooManyException(Exception):

    """
    More parameters than expected is an error.
    """

    pass
