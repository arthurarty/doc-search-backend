from app.clients.db_client import DocumentDbClient
from app.clients.google_cloud_client import GoogleCloudClient
from app.config import settings
from app.services.cloud_storage_service import CloudStorageService
from app.services.document_service import DocumentService

cloud_storage_service = CloudStorageService(
    bucket_name=settings.GCP_STORAGE_BUCKET_NAME,
    google_cloud_client=GoogleCloudClient(
        gcp_credentials_path=settings.GCP_SERVICE_ACCOUNT_PATH
    ),
)
document_service = DocumentService(
    cloud_storage_service=cloud_storage_service,
    org_file_db_client=DocumentDbClient(),
)
