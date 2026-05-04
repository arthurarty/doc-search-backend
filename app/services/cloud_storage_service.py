from collections.abc import Iterator

from app.clients.google_cloud_client import GoogleCloudClient
from app.schemas.cloud_storage_schemas import SignedUrlRequest, SignedUrlResponse


class CloudStorageService:
    """
    Orchestrator class for storing and retrieving files from storage.
    """

    def __init__(self, google_cloud_client: GoogleCloudClient, bucket_name: str):
        self.google_cloud_client = google_cloud_client
        self.bucket_name = bucket_name

    def create_upload_signed_url(
        self, file_upload: SignedUrlRequest
    ) -> SignedUrlResponse:
        """
        Create a signed url that can be used to upload a file.
        """
        blob_name = file_upload.blob_name
        signed_url = self.google_cloud_client.generate_upload_signed_url(
            bucket_name=self.bucket_name,
            blob_name=blob_name,
            content_type=file_upload.content_type,
            expiry_time=file_upload.expiry_time,
        )
        return SignedUrlResponse(
            signed_url=signed_url,
            blob_name=blob_name,
        )

    def read_blob_contents(self, blob_path: str) -> Iterator[str]:
        """
        Reads the blob contents, one page at a time.
        """
        yield from self.google_cloud_client.stream_file_contents(
            bucket_name=self.bucket_name,
            blob_path=blob_path,
        )
