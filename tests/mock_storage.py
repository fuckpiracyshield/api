from piracyshield_data_storage.blob.drivers.azure import AzureBlobStorage

import os

mock_storage = AzureBlobStorage(
    connection_string = os.environ.get("PIRACYSHIELD_MOCK_STORAGE_CONNECTION_STRING"),
    container_name = os.environ.get("PIRACYSHIELD_MOCK_STORAGE_CONTAINER_NAME")
)

mock_storage.create_container()
