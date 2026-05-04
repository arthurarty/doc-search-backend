import uuid
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.org_file_db_client import OrgFileDatabaseClient
from app.config import settings
from app.schemas.cloud_storage_schemas import SignedUrlRequest, SignedUrlResponse
from app.schemas.document_schemas import DocUploadRequest, OrgFileRecordResponse
from app.schemas.org_file_db_schemas import (
    CreateOrgFileRecordRequest,
    UpdateOrgFileRecordRequest,
)
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
        self, file_upload_request: DocUploadRequest, file_identifier: UUID
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
        self, db_session: AsyncSession, file_upload_request: DocUploadRequest
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
                file_size=file_upload_request.file_size,
                content_type=file_upload_request.content_type,
            ),
        )
        return signed_url_response

    async def get_org_file_by_unique_identifier(
        self, db_session: AsyncSession, unique_identifier: UUID
    ) -> OrgFileRecordResponse | None:
        """
        Get a single organization_file by its unique_identifier.
        """
        org_file = await self.org_file_db_client.get_by_unique_identifier(
            db_session, unique_identifier
        )
        if org_file:
            return OrgFileRecordResponse.model_validate(org_file)
        return None

    async def get_org_files(
        self, db_session: AsyncSession, skip: int | None = 0, limit: int | None = 25
    ) -> List[OrgFileRecordResponse]:
        org_files = await self.org_file_db_client.get_org_files(
            db_session, limit=limit, skip=skip
        )
        return [
            OrgFileRecordResponse.model_validate(org_file) for org_file in org_files
        ]

    async def update_document_status(
        self,
        db_session: AsyncSession,
        unique_identifier: UUID,
        update_request: UpdateOrgFileRecordRequest,
    ):
        pass
