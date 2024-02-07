from piracyshield_service.security.blacklist.exists_by_ip_address import SecurityBlacklistExistsByIPAddressService

from ioutils.errors import ErrorCode, ErrorMessage

class BlacklistInterceptor:

    """
    Applies bans.
    """

    security_blacklist_exists_by_ip_address_service = None

    async def execute(self, r):
        await self._prepare_modules()

        # if we have a valid IP address, let's check if it has been blacklisted
        if r.ip_address:
            if self.security_blacklist_exists_by_ip_address_service.execute(
                ip_address = r.ip_address
            ) == True:
                raise BlacklistInterceptorException()

    async def _prepare_modules(self):
        self.security_blacklist_exists_by_ip_address_service = SecurityBlacklistExistsByIPAddressService()

class BlacklistInterceptorException(Exception):

    """
    The IP address is temporary banned.
    """

    status_code = 403

    error_code = ErrorCode.IP_ADDRESS_BLACKLISTED

    error_message = ErrorMessage.IP_ADDRESS_BLACKLISTED
