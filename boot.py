import tornado.ioloop

from piracyshield_component.config import Config
from piracyshield_component.environment import Environment

from v1.routes import APIv1

from application import Application

api_config = Config('api').get('general')

if __name__ == "__main__":
    app = Application(
        # wether to run the application using debug mode
        debug = api_config['debug'],

        # load current routes
        handlers = APIv1.routes,

        # adds a standard version prefix
        version = api_config['version'],

        # sets a prefix for each route
        prefix = api_config['prefix'],

        # cookie secret
        cookie_secret = api_config['cookie_secret'],

        # cache absolute location
        cache_path = Environment.CACHE_PATH
    )

    http_server = tornado.httpserver.HTTPServer(app, xheaders = True)

    http_server.listen(api_config['port'])

    tornado.ioloop.IOLoop.instance().start()
