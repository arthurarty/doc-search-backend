from app.clients.google_cloud_client import GoogleCloudClient
from app.config import settings


class CloudStorageService:
    """
    Orchestrator class for storing and retrieving files from storage.
    """
    def __init__(self, google_cloud_client: GoogleCloudClient, bucket_name: str):
        self.google_cloud_client = google_cloud_client
        self.bucket_name = bucket_name

    def create_upload_signed_url(self) -> str:
        """
        Create a signed url that can be used to upload a file.
        """
        blob_name = "file-upload-12.pdf"
        return self.google_cloud_client.generate_upload_signed_url(
            bucket_name=self.bucket_name,
            blob_name=blob_name,
            expiry_time=settings.signed_url_expiry_time
        )
