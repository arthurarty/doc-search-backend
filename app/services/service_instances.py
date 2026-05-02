from app.clients.google_cloud_client import GoogleCloudClient
from app.config import settings
from app.services.cloud_storage_service import CloudStorageService

cloud_storage_service = CloudStorageService(
    bucket_name=settings.gcp_storage_bucket_name,
    google_cloud_client=GoogleCloudClient(
        gcp_credentials_path=settings.gcp_service_account_path
    ),
)
