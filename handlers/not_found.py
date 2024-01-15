import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ioutils.request import RequestHandler
from ioutils.errors import ErrorCode, ErrorMessage

class NotFoundHandler(RequestHandler):

    """
    Handle for 404 routes.
    """

    def prepare(self):
        self.error(status_code = 404, error_code = ErrorCode.ROUTE_NOT_FOUND, message = ErrorMessage.ROUTE_NOT_FOUND)
