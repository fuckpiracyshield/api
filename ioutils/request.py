from piracyshield_component.log.logger import Logger
from piracyshield_component.exception import ApplicationException
from .response import ResponseHandler

import time
from collections import deque
from tornado.locks import Lock

from interceptors.logger import LoggerInterceptor
from interceptors.security.blacklist import BlacklistInterceptor
from interceptors.security.rate_limit import RateLimitInterceptor

from ioutils.errors import ErrorCode, ErrorMessage

class RequestHandler(ResponseHandler):

    """
    Requests gateway.

    The requestor gets blocked here before proceding any further.
    Interceptors are implemented to allow certain features to take part of the action.

    Current actived interceptors:
      - security: takes care of the IP addresses exceeding limits (ex. applies the ban rules when triggered).
      - rate limit: the IP will get a 429 when trying to perform too many requests on a given timeframe.
    """

    interceptors = [
        LoggerInterceptor,
        BlacklistInterceptor,
        RateLimitInterceptor
    ]

    ip_address = None

    async def prepare(self):
        self.ip_address = self.request.remote_ip

        # honor the IP passed via reverse proxy
        if 'X-Forwarded-For' in self.request.headers:
            # TODO: we need validation as this could be easily spoofed.

            # we could have multiple IPs here
            forwarded_ip_addresses = str(self.request.headers.get("X-Forwarded-For")).split(',')

            # get only the forwarded client IP
            self.ip_address = forwarded_ip_addresses[0]

            # if any port is specified just ignore it and keep only the IP
            self.ip_address.split(':')[0]

        await self.run_interceptors()

    async def run_interceptors(self):
        for interceptor in self.interceptors:
            try:
                await interceptor().execute(self)

            except Exception as InterceptorException:
                self.error(
                    status_code = InterceptorException.status_code,
                    error_code = InterceptorException.error_code,
                    message = InterceptorException.error_message
                )

                return
