import datetime
from collections.abc import Iterator

from google.cloud import storage
from google.oauth2 import service_account
from pypdf import PdfReader


class GoogleCloudClient:
    """
    A client for interacting with Google Cloud Platform services
    """

    def __init__(self, gcp_credentials_path: str):
        self.credentials = service_account.Credentials.from_service_account_file(
            gcp_credentials_path
        )

    def generate_upload_signed_url(
        self,
        bucket_name: str,
        blob_name: str,
        content_type: str | None = "application/octet-stream",
        expiry_time: int | None = 15,
    ):
        """Generates a v4 signed URL for uploading a blob using HTTP PUT.

        Expire_time is in minutes and determines how long a URL is valid for.
        """
        storage_client = storage.Client(credentials=self.credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiry_time),
            method="PUT",
            content_type=content_type,
        )
        return url

    def stream_file_contents(self, bucket_name: str, blob_path: str) -> Iterator[str]:
        """
        Reads a single page at a time and yields its text.
        """
        storage_client = storage.Client(credentials=self.credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        with blob.open("rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                yield text
