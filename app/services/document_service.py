import uuid
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.org_file_db_client import OrgFileDatabaseClient
from app.config import settings
from app.schemas.cloud_storage_schemas import SignedUrlRequest, SignedUrlResponse
from app.schemas.file_upload_schemas import FileUploadRequest
from app.schemas.org_file_db_schemas import CreateOrgFileRecordRequest
from app.services.cloud_storage_service import CloudStorageService
from app.utils.file_utils import get_file_extension


class DocumentService:
    """
    Orchestrator class for handling documents.
    """

    def __init__(
        self,
        org_file_db_client: OrgFileDatabaseClient,
        cloud_storage_service: CloudStorageService,
    ):
        self.org_file_db_client = org_file_db_client
        self.cloud_storage_service = cloud_storage_service

    def create_signed_url(
        self, file_upload_request: FileUploadRequest, file_identifier: UUID
    ) -> SignedUrlResponse:
        file_extension = get_file_extension(file_upload_request.file_name)
        blob_name = f"{file_identifier.hex}.{file_extension}"
        signed_url_request = SignedUrlRequest(
            blob_name=blob_name,
            content_type=file_upload_request.content_type,
            expiry_time=settings.SIGNED_URL_EXPIRY_TIME,
        )
        return self.cloud_storage_service.create_upload_signed_url(
            file_upload=signed_url_request
        )

    async def process_file_upload(
        self, db_session: AsyncSession, file_upload_request: FileUploadRequest
    ) -> SignedUrlResponse:
        """
        Creates a signed url that can be used to upload a file.
        Creates database entry in the OrganizationFile table.
        """
        file_identifier = uuid.uuid4()
        signed_url_response = self.create_signed_url(
            file_upload_request, file_identifier
        )
        # Todo: Add exception handling for signed_url creation
        await self.org_file_db_client.create(
            db_session=db_session,
            org_file_request=CreateOrgFileRecordRequest(
                file_name=file_upload_request.file_name,
                unique_identifier=file_identifier,
            ),
        )
        return signed_url_response
