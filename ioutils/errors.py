
class ErrorCode:

    """
    API error codes.
    """

    GENERIC = '1000'

    PERMISSION_DENIED = '1001'

    FORBIDDEN = '1002'

    ROUTE_NOT_FOUND = '1003'

    METHOD_NOT_ALLOWED = '1004'

    TOO_MANY_REQUESTS = '1005'

    MISSING_TOKEN = '1006'

    MISSING_REFRESH_TOKEN = '1007'

    TOKEN_FORMAT_NON_VALID = '1008'

    NON_VALID_PARAMETERS = '1009'

    MISSING_PARAMETERS = '1010'

    TOO_MANY_PARAMETERS = '1011'

    MISSING_FILE = '1012'

    NO_DATA_AVAILABLE = '1013'

    CHANGE_PASSWORD = '1014'

class ErrorMessage:

    """
    API error messages.
    """

    GENERIC = 'Generic application error.'

    PERMISSION_DENIED = "Permission denied."

    # routing

    FORBIDDEN = 'Forbidden.'

    ROUTE_NOT_FOUND = 'Route not found.'

    METHOD_NOT_ALLOWED = 'Method not allowed.'

    TOO_MANY_REQUESTS = 'Too many requests.'

    # jwt token

    MISSING_TOKEN = 'Missing authentication token.'

    MISSING_REFRESH_TOKEN = 'Missing refresh token from cookie or POST parameters.'

    TOKEN_FORMAT_NON_VALID = 'Token format non valid.'

    # json POST parameters

    NON_VALID_PARAMETERS = 'Expecting JSON data.'

    MISSING_PARAMETERS = 'Missing required parameters.'

    TOO_MANY_PARAMETERS = 'Too many parameters.'

    # files

    MISSING_FILE = 'Missing required file.'

    NO_DATA_AVAILABLE = 'No data available for this request.'

    # account settings

    CHANGE_PASSWORD = 'A password change has been activated for your account. You must first authenticate via web app and follow the instructions.'
