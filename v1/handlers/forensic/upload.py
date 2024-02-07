import os
import json
import tornado

from ioutils.protected import ProtectedHandler
from ioutils.errors import ErrorCode, ErrorMessage
from piracyshield_service.forensic.create_archive import ForensicCreateArchiveService
from piracyshield_component.environment import Environment
from piracyshield_component.exception import ApplicationException

class UploadForensicHandler(ProtectedHandler):

    def get_received_chunks_info_path(self, filename):
        return f"{Environment.CACHE_PATH}/{filename}_info.json"

    def update_received_chunks_info(self, filename, chunk_index):
        info_path = self.get_received_chunks_info_path(filename)

        if os.path.exists(info_path):
            with open(info_path, 'r') as file:
                info = json.load(file)

                received_chunks = set(info['received_chunks'])
        else:
            received_chunks = set()

        received_chunks.add(chunk_index)

        with open(info_path, 'w') as file:
            json.dump({"received_chunks": list(received_chunks)}, file)

    def check_all_chunks_received(self, filename, total_chunks):
        info_path = self.get_received_chunks_info_path(filename)

        if os.path.exists(info_path):
            with open(info_path, 'r') as file:
                info = json.load(file)

                return len(info['received_chunks']) == total_chunks

        return False

    async def post(self, ticket_id):
        if not self.initialize_account():
            return

        # verify permissions
        self.permission_service.can_upload_ticket()

        if 'archive' not in self.request.files or 'chunkIndex' not in self.request.arguments or 'totalChunks' not in self.request.arguments:
            return self.error(status_code = 400, error_code = ErrorCode.MISSING_FILE, message = ErrorMessage.MISSING_FILE)

        try:
            archive_handler = self.request.files['archive'][0]
            chunk_index = int(self.request.arguments['chunkIndex'][0])
            total_chunks = int(self.request.arguments['totalChunks'][0])
            original_filename = self.get_argument('originalFileName')

            filename = f"{ticket_id}_{original_filename}"

            temp_storage_path = f"{Environment.CACHE_PATH}/{filename}"

            chunk_temp_path = temp_storage_path + f"_part{chunk_index}"

            with open(chunk_temp_path, "wb") as temp_file:
                temp_file.write(archive_handler['body'])

            # update received chunks
            self.update_received_chunks_info(filename, chunk_index)

            # did we get every chunk?
            if self.check_all_chunks_received(filename, total_chunks):
                # proceed to assemble all the chunks into the a single file
                with open(temp_storage_path, "wb") as final_file:
                    for i in range(total_chunks):
                        part_file_path = temp_storage_path + f"_part{i}"

                        if not os.path.exists(part_file_path):
                            raise ApplicationException("Missing file chunk: " + str(i))

                        with open(part_file_path, "rb") as part_file:
                            final_file.write(part_file.read())

                        os.remove(part_file_path)

                # process the final file
                forensic_create_archive_service = ForensicCreateArchiveService()

                await tornado.ioloop.IOLoop.current().run_in_executor(
                    None,
                    forensic_create_archive_service.execute,
                    ticket_id,
                    filename
                )

                # clean stored info
                os.remove(self.get_received_chunks_info_path(filename))

            # always answer or the frontend won't send anything more
            self.success()

        except ApplicationException as e:
            self.error(status_code = 400, error_code = e.code, message = e.message)
