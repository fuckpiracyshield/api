from .handlers.authentication.login import AuthenticationLoginHandler
from .handlers.authentication.refresh import AuthenticationRefreshHandler
from .handlers.authentication.logout import AuthenticationLogoutHandler

from .handlers.account.get import GetGeneralAccountHandler
from .handlers.account.get_all import GetAllGeneralAccountHandler

from .handlers.account.guest.create import CreateGuestAccountHandler
from .handlers.account.guest.get import GetGuestAccountHandler
from .handlers.account.guest.get_all import GetAllGuestAccountHandler
from .handlers.account.guest.remove import RemoveGuestAccountHandler

from .handlers.account.internal.create import CreateInternalAccountHandler
from .handlers.account.internal.get import GetInternalAccountHandler
from .handlers.account.internal.get_all import GetAllInternalAccountHandler
from .handlers.account.internal.set_status import SetStatusActiveInternalAccountHandler, SetStatusNonActiveInternalAccountHandler
from .handlers.account.internal.change_password import ChangePasswordInternalAccountHandler
from .handlers.account.internal.remove import RemoveInternalAccountHandler

from .handlers.account.reporter.create import CreateReporterAccountHandler
from .handlers.account.reporter.get import GetReporterAccountHandler
from .handlers.account.reporter.get_all import GetAllReporterAccountHandler
from .handlers.account.reporter.set_status import SetStatusActiveReporterAccountHandler, SetStatusNonActiveReporterAccountHandler
from .handlers.account.reporter.change_password import ChangePasswordReporterAccountHandler
from .handlers.account.reporter.remove import RemoveReporterAccountHandler

from .handlers.account.provider.create import CreateProviderAccountHandler
from .handlers.account.provider.get import GetProviderAccountHandler
from .handlers.account.provider.get_all import GetAllProviderAccountHandler
from .handlers.account.provider.set_status import SetStatusActiveProviderAccountHandler, SetStatusNonActiveProviderAccountHandler
from .handlers.account.provider.change_password import ChangePasswordProviderAccountHandler
from .handlers.account.provider.remove import RemoveProviderAccountHandler

from .handlers.account.session.get_all import GetAllSessionAccountHandler

from .handlers.ticket.create import CreateTicketHandler
from .handlers.ticket.get import GetTicketHandler
from .handlers.ticket.get_all import GetAllTicketHandler
from .handlers.ticket.get_total import GetTotalTicketHandler
from .handlers.ticket.remove import RemoveTicketHandler

from .handlers.ticket.error.create import CreateTicketErrorHandler
from .handlers.ticket.error.get_by_ticket import GetByTicketTicketErrorHandler
from .handlers.ticket.error.get_by_account import GetByReporterTicketErrorHandler

from .handlers.forensic.upload import UploadForensicHandler
from .handlers.forensic.get_by_ticket import GetByTicketForensicHandler
from .handlers.forensic.get_supported_formats import GetSupportedFormatsForensicHandler
from .handlers.forensic.get_supported_hashes import GetSupportedHashesForensicHandler

from .handlers.ticket.item.set_processed import SetTicketItemProcessedHandler
from .handlers.ticket.item.set_unprocessed import SetTicketItemUnprocessedHandler

from .handlers.ticket.item.set_flag_active import SetFlagActiveTicketItemHandler, SetFlagNonActiveTicketItemHandler

from .handlers.ticket.item.get_all_status import GetAllStatusTicketItemHandler
from .handlers.ticket.item.get_all import GetAllTicketItemHandler
from .handlers.ticket.item.get_available_by_ticket import GetAvailableByTicketTicketItemHandler
from .handlers.ticket.item.get_details import GetDetailsTicketItemHandler

from .handlers.ticket.item.fqdn.get_all import GetAllFQDNHandler
from .handlers.ticket.item.fqdn.get_all_txt import GetAllFQDNTXTHandler
from .handlers.ticket.item.fqdn.get_all_by_ticket import GetTicketFQDNHandler
from .handlers.ticket.item.fqdn.get_all_by_ticket_txt import GetTicketFQDNTXTHandler
from .handlers.ticket.item.fqdn.get_all_by_ticket_checksum_txt import GetTicketFQDNTXTChecksumHandler
from .handlers.ticket.item.fqdn.get_all_checksum_txt import GetAllFQDNTXTChecksumHandler

from .handlers.ticket.item.ipv4.get_all import GetAllIPv4Handler
from .handlers.ticket.item.ipv4.get_all_txt import GetAllIPv4TXTHandler
from .handlers.ticket.item.ipv4.get_all_by_ticket import GetTicketIPv4Handler
from .handlers.ticket.item.ipv4.get_all_by_ticket_txt import GetTicketIPv4TXTHandler
from .handlers.ticket.item.ipv4.get_all_by_ticket_checksum_txt import GetTicketIPv4TXTChecksumHandler
from .handlers.ticket.item.ipv4.get_all_checksum_txt import GetAllIPv4TXTChecksumHandler

from .handlers.ticket.item.ipv6.get_all import GetAllIPv6Handler
from .handlers.ticket.item.ipv6.get_all_txt import GetAllIPv6TXTHandler
from .handlers.ticket.item.ipv6.get_all_by_ticket import GetTicketIPv6Handler
from .handlers.ticket.item.ipv6.get_all_by_ticket_txt import GetTicketIPv6TXTHandler
from .handlers.ticket.item.ipv6.get_all_by_ticket_checksum_txt import GetTicketIPv6TXTChecksumHandler
from .handlers.ticket.item.ipv6.get_all_checksum_txt import GetAllIPv6TXTChecksumHandler

from .handlers.whitelist.create import CreateWhitelistItemHandler
from .handlers.whitelist.get_all import GetAllWhitelistItemHandler
from .handlers.whitelist.get_all_by_account import GetAllByAccountWhitelistItemHandler
from .handlers.whitelist.get_global import GetGlobalWhitelistItemHandler
from .handlers.whitelist.set_status import SetStatusActiveWhitelistItemHandler, SetStatusNonActiveWhitelistItemHandler
from .handlers.whitelist.remove import RemoveWhitelistItemHandler

from .handlers.dda.create import CreateDDAHandler
from .handlers.dda.get_all import GetAllDDAHandler
from .handlers.dda.get_all_by_account import GetAllByAccountDDAHandler
from .handlers.dda.get_global import GetGlobalDDAHandler
from .handlers.dda.set_status import SetStatusActiveDDAHandler, SetStatusNonActiveDDAHandler
from .handlers.dda.remove import RemoveDDAHandler

from .handlers.log.ticket.get_all import GetAllTicketLogHandler
from .handlers.log.ticket.item.get_all import GetAllTicketItemLogHandler

class APIv1:

    routes = [
        # authentication
        (r"/authentication/login", AuthenticationLoginHandler),
        (r"/authentication/refresh", AuthenticationRefreshHandler),
        (r"/authentication/logout", AuthenticationLogoutHandler),

        # global account management
        (r"/account/get", GetGeneralAccountHandler),
        (r"/account/get/all", GetAllGeneralAccountHandler),

        # guest account management
        (r"/account/guest/create", CreateGuestAccountHandler),
        (r"/account/guest/get", GetGuestAccountHandler),
        (r"/account/guest/get/all", GetAllGuestAccountHandler),
        (r"/account/guest/remove", RemoveGuestAccountHandler),

        # internal account management
        (r"/account/internal/create", CreateInternalAccountHandler),
        (r"/account/internal/get", GetInternalAccountHandler),
        (r"/account/internal/get/all", GetAllInternalAccountHandler),
        (r"/account/internal/set/status/active", SetStatusActiveInternalAccountHandler),
        (r"/account/internal/set/status/non_active", SetStatusNonActiveInternalAccountHandler),
        (r"/account/internal/change_password", ChangePasswordInternalAccountHandler),
        (r"/account/internal/remove", RemoveInternalAccountHandler),

        # reporter account management
        (r"/account/reporter/create", CreateReporterAccountHandler),
        (r"/account/reporter/get", GetReporterAccountHandler),
        (r"/account/reporter/get/all", GetAllReporterAccountHandler),
        (r"/account/reporter/set/status/active", SetStatusActiveReporterAccountHandler),
        (r"/account/reporter/set/status/non_active", SetStatusNonActiveReporterAccountHandler),
        (r"/account/reporter/change_password", ChangePasswordReporterAccountHandler),
        (r"/account/reporter/remove", RemoveReporterAccountHandler),

        # provider account management
        (r"/account/provider/create", CreateProviderAccountHandler),
        (r"/account/provider/get", GetProviderAccountHandler),
        (r"/account/provider/get/all", GetAllProviderAccountHandler),
        (r"/account/provider/set/status/active", SetStatusActiveProviderAccountHandler),
        (r"/account/provider/set/status/non_active", SetStatusNonActiveProviderAccountHandler),
        (r"/account/provider/change_password", ChangePasswordProviderAccountHandler),
        (r"/account/provider/remove", RemoveProviderAccountHandler),

        # sessions
        (r"/account/session/get/all", GetAllSessionAccountHandler),

        # blocking ticket management
        (r"/ticket/create", CreateTicketHandler),
        (r"/ticket/get", GetTicketHandler),
        (r"/ticket/get/all", GetAllTicketHandler),
        (r"/ticket/remove", RemoveTicketHandler),
        (r"/ticket/item/get/all", GetAllTicketItemHandler),
        (r"/ticket/item/get/available/by_ticket", GetAvailableByTicketTicketItemHandler),

        # error ticket management
        (r"/ticket/error/create", CreateTicketErrorHandler),
        (r"/ticket/error/get/by_ticket", GetByTicketTicketErrorHandler),
        (r"/ticket/error/get", GetByReporterTicketErrorHandler),

        # internal use only
        (r"/ticket/get/total", GetTotalTicketHandler),
        (r"/ticket/item/status/get/all", GetAllStatusTicketItemHandler),
        (r"/ticket/item/get/details", GetDetailsTicketItemHandler),

        (r"/ticket/get/fqdn", GetTicketFQDNHandler),
        (r"/ticket/get/fqdn/txt", GetTicketFQDNTXTHandler),
        (r"/ticket/get/fqdn/txt/checksum", GetTicketFQDNTXTChecksumHandler),

        (r"/ticket/get/ipv4", GetTicketIPv4Handler),
        (r"/ticket/get/ipv4/txt", GetTicketIPv4TXTHandler),
        (r"/ticket/get/ipv4/txt/checksum", GetTicketIPv4TXTChecksumHandler),

        (r"/ticket/get/ipv6", GetTicketIPv6Handler),
        (r"/ticket/get/ipv6/txt", GetTicketIPv6TXTHandler),
        (r"/ticket/get/ipv6/txt/checksum", GetTicketIPv6TXTChecksumHandler),

        (r"/ticket/item/set/processed", SetTicketItemProcessedHandler),
        (r"/ticket/item/set/unprocessed", SetTicketItemUnprocessedHandler),

        (r"/ticket/item/set/active", SetFlagActiveTicketItemHandler),
        (r"/ticket/item/set/non_active", SetFlagNonActiveTicketItemHandler),

        # FQDN item management
        (r"/fqdn/get/all", GetAllFQDNHandler),
        (r"/fqdn/get/all/txt", GetAllFQDNTXTHandler),
        (r"/fqdn/get/all/txt/checksum", GetAllFQDNTXTChecksumHandler),

        # IPv4 item management
        (r"/ipv4/get/all", GetAllIPv4Handler),
        (r"/ipv4/get/all/txt", GetAllIPv4TXTHandler),
        (r"/ipv4/get/all/txt/checksum", GetAllIPv4TXTChecksumHandler),

        # IPv6 item management
        (r"/ipv6/get/all", GetAllIPv6Handler),
        (r"/ipv6/get/all/txt", GetAllIPv6TXTHandler),
        (r"/ipv6/get/all/txt/checksum", GetAllIPv6TXTChecksumHandler),

        # forensic evidence management
        (r"/forensic/upload/([a-zA-Z0-9]+)", UploadForensicHandler),
        (r"/forensic/get/by_ticket", GetByTicketForensicHandler),
        (r"/forensic/get/supported_formats", GetSupportedFormatsForensicHandler),
        (r"/forensic/get/supported_hashes", GetSupportedHashesForensicHandler),

        # whitelist management
        (r"/whitelist/item/create", CreateWhitelistItemHandler),
        (r"/whitelist/item/get/all", GetAllWhitelistItemHandler),
        (r"/whitelist/item/get/all/by_account", GetAllByAccountWhitelistItemHandler),
        (r"/whitelist/item/get/global", GetGlobalWhitelistItemHandler),
        (r"/whitelist/item/set/status/active", SetStatusActiveWhitelistItemHandler),
        (r"/whitelist/item/set/status/non_active", SetStatusNonActiveWhitelistItemHandler),
        (r"/whitelist/item/remove", RemoveWhitelistItemHandler),

        # DDA management
        (r"/dda/create", CreateDDAHandler),
        (r"/dda/get/all", GetAllDDAHandler),
        (r"/dda/get/all/by_account", GetAllByAccountDDAHandler),
        (r"/dda/get/global", GetGlobalDDAHandler),
        (r"/dda/set/status/active", SetStatusActiveDDAHandler),
        (r"/dda/set/status/non_active", SetStatusNonActiveDDAHandler),
        (r"/dda/remove", RemoveDDAHandler),

        # ticket logging management
        (r"/log/ticket/get/all", GetAllTicketLogHandler)
    ]
