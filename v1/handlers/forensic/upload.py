import sys
import os

# I hate python imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage

from piracyshield_service.forensic.create_archive import ForensicCreateArchiveService

from piracyshield_component.exception import ApplicationException

class UploadForensicHandler(ProtectedHandler):

    """
    Appends the forensic evidence.
    """

    async def post(self, ticket_id):
        if self.initialize_account() == False:
            return

        # verify permissions
        self.permission_service.can_upload_ticket()

        # TODO: we could add some mime type filters but we might need to interrogate the ticket model to have a dynamic implementation.

        # no archive passed?
        if 'archive' not in self.request.files:
            return self.error(status_code = 400, error_code = ErrorCode.MISSING_FILE, message = ErrorMessage.MISSING_FILE)

        # get the file data
        archive_handler = self.request.files['archive'][0]

        try:
            forensic_create_archive_service = ForensicCreateArchiveService()

            await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                forensic_create_archive_service.execute,
                ticket_id,
                archive_handler['filename'],
                archive_handler['body']
            )

            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
