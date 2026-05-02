from app.clients.google_cloud_client import GoogleCloudClient
from app.config import settings
from app.services.cloud_storage_service import CloudStorageService

cloud_storage_service = CloudStorageService(
    bucket_name=settings.GCP_STORAGE_BUCKET_NAME,
    google_cloud_client=GoogleCloudClient(
        gcp_credentials_path=settings.GCP_SERVICE_ACCOUNT_PATH
    ),
)
