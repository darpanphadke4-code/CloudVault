import uuid
from azure.storage.blob import BlobServiceClient
from flask import current_app


def get_blob_service():
    connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
    return BlobServiceClient.from_connection_string(connection_string)


def upload_file(file):

    blob_service = get_blob_service()

    container = current_app.config["AZURE_CONTAINER_NAME"]

    blob_name = f"{uuid.uuid4()}_{file.filename}"

    blob_client = blob_service.get_blob_client(
        container=container,
        blob=blob_name
    )

    blob_client.upload_blob(
        file,
        overwrite=False
    )

    return {
        "blob_name": blob_name,
        "content_type": file.content_type
    }


def delete_file(blob_name):

    blob_service = get_blob_service()

    container = current_app.config["AZURE_CONTAINER_NAME"]

    blob_client = blob_service.get_blob_client(
        container=container,
        blob=blob_name
    )

    blob_client.delete_blob()

def get_blob_client(blob_name):

    blob_service = get_blob_service()

    container = current_app.config["AZURE_CONTAINER_NAME"]

    return blob_service.get_blob_client(
        container=container,
        blob=blob_name
    )


def download_blob(blob_name):

    blob_service = get_blob_service()

    container = current_app.config["AZURE_CONTAINER_NAME"]

    blob_client = blob_service.get_blob_client(
        container=container,
        blob=blob_name
    )

    return blob_client.download_blob().readall()

