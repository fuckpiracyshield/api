from piracyshield_component.log.logger import Logger

import tornado

from handlers.ping import PingHandler
from handlers.not_found import NotFoundHandler

class Application(tornado.web.Application):

    """
    Application initializer.
    """

    def __init__(self, debug: bool, handlers: list, version: str, prefix: str, cookie_secret: str, cache_path: str):
        """
        This is a list of handlers that directly extend the RequestHandler class, instead of relying on a BaseHandler class.

        :param handlers: list of handlers based on a BaseHandler class.
        :param version: version of the API (ex. "v1").
        :param handlers: API url prefix (ex. "/api").
        :param cookie_secret: this is a secret to provide more security for the cookie signing when they are set.
        :param cache_path: folder for cache uploads.
        :return: a list of routes and their handlers.
        """

        if prefix:
            version = f'{prefix}/{version}'

        # checks if the prefix option is set and starts adding the custom prefix to each route
        handlers = [(version + handle[0], handle[1]) for handle in handlers]

        complete_handlers = handlers + self._get_default_handlers()

        self.logger = Logger('api')

        self.logger.info('Started')

        tornado.web.Application.__init__(
            self,
            debug = debug,
            handlers = complete_handlers,
            cookie_secret = cookie_secret,
            cache_path = cache_path
        )

    def _get_default_handlers(self) -> list:
        """
        This is a list of handlers that directly extend the RequestHandler class, instead of relying on a BaseHandler class.

        :return: a list of routes and their handlers.
        """

        return [
            (r'/api/v1/ping', PingHandler),
            (r'.*', NotFoundHandler)
        ]
