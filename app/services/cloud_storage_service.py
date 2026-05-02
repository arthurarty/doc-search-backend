import uuid

from app.clients.google_cloud_client import GoogleCloudClient
from app.config import settings
from app.schemas.cloud_storage_schemas import FileUploadRequest, SignedUrlResponse
from app.utils.file_utils import get_file_extension


class CloudStorageService:
    """
    Orchestrator class for storing and retrieving files from storage.
    """

    def __init__(self, google_cloud_client: GoogleCloudClient, bucket_name: str):
        self.google_cloud_client = google_cloud_client
        self.bucket_name = bucket_name

    def create_upload_signed_url(
        self, file_upload: FileUploadRequest
    ) -> SignedUrlResponse:
        """
        Create a signed url that can be used to upload a file.
        """
        file_identifier = uuid.uuid4()
        file_extension = get_file_extension(file_upload.file_name)
        blob_name = f"{file_identifier.hex}.{file_extension}"
        signed_url = self.google_cloud_client.generate_upload_signed_url(
            bucket_name=self.bucket_name,
            blob_name=blob_name,
            content_type=file_upload.content_type,
            expiry_time=settings.signed_url_expiry_time,
        )
        return SignedUrlResponse(
            signed_url=signed_url,
            blob_name=blob_name,
        )
