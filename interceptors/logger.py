from piracyshield_component.log.logger import Logger

class LoggerInterceptor:

    """
    Logs requests
    """

    async def execute(self, r):
        r.application.logger.debug(f'> GET `{r.request.uri}` from `{r.request.remote_ip}`')

class LoggerInterceptorException(Exception):

    """
    We need this as a placeholder.
    """

    pass
