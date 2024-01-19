from tornado.locks import Lock
from collections import deque
import time

from ioutils.errors import ErrorCode, ErrorMessage

class RateLimitInterceptor:

    """
    Blocks flooding.
    """

    # override the default methods
    SUPPORTED_METHODS = ("GET", "POST")

    # max requests allowed in a second
    MAX_REQUESTS_PER_SECOND = 100

    # requests container
    REQUESTS = {}

    # needs a mutex to manage the async threads writes
    mutex = Lock()

    async def execute(self, _):
        # get the current timestamp in seconds
        timestamp = int(time.time())

        async with self.mutex:
            if timestamp not in self.REQUESTS:
                self.REQUESTS[timestamp] = deque(maxlen = self.MAX_REQUESTS_PER_SECOND)

            # check if we exceeded the rate limit
            if len(self.REQUESTS[timestamp]) >= self.MAX_REQUESTS_PER_SECOND:
                raise RateLimitInterceptorException()

            # add the current request
            self.REQUESTS[timestamp].append(time.time())

        # trigger the old timestamps cleaning
        await self._clean_timestamps(timestamp)

    async def _clean_timestamps(self, current_timestamp):
        """
        Cleanup the old timestamps that are no longer relevant.

        NOTE: this is quite inefficient and slow for Python, but that's all we can do to manage this in the application.

        :param current_timestamp: current timestamp.
        """

        async with self.mutex:
            # keep only the keys for the current and previous second
            for timestamp in list(self.REQUESTS.keys()):
                if timestamp < current_timestamp - 1:
                    del self.REQUESTS[timestamp]

class RateLimitInterceptorException(Exception):

    """
    Too many requests.
    """

    status_code = 429

    error_code = ErrorCode.TOO_MANY_REQUESTS

    error_message = ErrorMessage.TOO_MANY_REQUESTS
