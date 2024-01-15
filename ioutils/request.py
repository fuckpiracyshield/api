from piracyshield_component.log.logger import Logger
from piracyshield_component.exception import ApplicationException

from .response import ResponseHandler

import tornado.web
import time

class RequestHandler(ResponseHandler):

    """
    Requests gateway.
    """

    # override the default methods
    SUPPORTED_METHODS = ("GET", "POST")

    # max requests allowed in a second
    MAX_REQUESTS_PER_SECOND = 100

    # requests container
    REQUESTS = {}

    def prepare(self) -> None:
        """
        Handles the request general procedures.
        This method implements a very simple request limit check.
        """

        self.application.logger.debug(f'> GET `{self.request.uri}` from `{self.request.remote_ip}`')

        # get the current timestamp in seconds
        timestamp = int(time.time())

        # TODO: this should be better handled and also provide a way to temporary ban each IP when flooding.

        # check if the number of requests for this second has exceeded the limit
        if timestamp in self.REQUESTS:
            if self.REQUESTS[timestamp] >= self.MAX_REQUESTS_PER_SECOND:
                self.error(status_code = 429, error_code = ErrorCode.TOO_MANY_REQUESTS, message = ErrorMessage.TOO_MANY_REQUESTS)

                return

        # increment the number of requests for this second
        self.REQUESTS[timestamp] = self.REQUESTS.get(timestamp, 0) + 1

        # decrement the number of requests after one second
        tornado.ioloop.IOLoop.current().call_later(1.0, self._decrement_requests_count, timestamp)

    def _decrement_requests_count(self, timestamp):
        """
        Decrement the requests count per timestamp.

        :param timestamp: current timestamp.
        """

        if timestamp in self.REQUESTS:
            self.REQUESTS[timestamp] -= 1
