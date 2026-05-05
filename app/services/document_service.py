import uuid
from typing import List
from uuid import UUID

from langchain_ollama import OllamaEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.db_client import DocumentDbClient
from app.config import settings
from app.models.documents import DocumentStatusEnum
from app.schemas.cloud_storage_schemas import SignedUrlRequest, SignedUrlResponse
from app.schemas.document_schemas import (
    CreateDocRequest,
    CreateDocResponse,
    CreateOrgFileRecordRequest,
    DocResponse,
    SemanticSearchResponse,
    UpdateDocRequest,
    UpdateOrgFileRecordRequest,
)
from app.services.cloud_storage_service import CloudStorageService
from app.tasks.index_file import process_document
from app.utils.file_utils import get_blob_name


class DocumentService:
    """
    Orchestrator class for handling documents.
    """

    def __init__(
        self,
        db_client: DocumentDbClient,
        cloud_storage_service: CloudStorageService,
    ):
        self.db_client = db_client
        self.cloud_storage_service = cloud_storage_service
        self.embeddings_model = OllamaEmbeddings(
            model=settings.EMBEDDINGS_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )

    def create_signed_url(
        self, file_upload_request: CreateDocRequest, file_identifier: UUID
    ) -> SignedUrlResponse:
        blob_name = get_blob_name(file_identifier, file_upload_request.file_name)
        signed_url_request = SignedUrlRequest(
            blob_name=blob_name,
            content_type=file_upload_request.content_type,
            expiry_time=settings.SIGNED_URL_EXPIRY_TIME,
        )
        return self.cloud_storage_service.create_upload_signed_url(
            file_upload=signed_url_request
        )

    async def process_file_upload(
        self, db_session: AsyncSession, file_upload_request: CreateDocRequest
    ) -> CreateDocResponse:
        """
        Creates a signed url that can be used to upload a file.
        Creates database entry in the OrganizationFile table.
        """
        file_identifier = uuid.uuid7()
        signed_url_response = self.create_signed_url(
            file_upload_request, file_identifier
        )
        # Todo: Add exception handling for signed_url creation
        await self.db_client.create_document(
            db_session=db_session,
            org_file_request=CreateOrgFileRecordRequest(
                file_name=file_upload_request.file_name,
                unique_identifier=file_identifier,
                file_size=file_upload_request.file_size,
                content_type=file_upload_request.content_type,
            ),
        )
        return CreateDocResponse(
            blob_name=signed_url_response.blob_name,
            signed_url=signed_url_response.signed_url,
            unique_identifier=file_identifier,
        )

    async def get_document_by_unique_identifier(
        self, db_session: AsyncSession, unique_identifier: UUID
    ) -> DocResponse | None:
        """
        Get a single organization_file by its unique_identifier.
        """
        document = await self.db_client.get_by_unique_identifier(
            db_session, unique_identifier
        )
        if document:
            return DocResponse.model_validate(document)
        return None

    async def get_documents(
        self, db_session: AsyncSession, skip: int | None = 0, limit: int | None = 25
    ) -> List[DocResponse]:
        documents = await self.db_client.get_documents(
            db_session, limit=limit, skip=skip
        )
        return [DocResponse.model_validate(document) for document in documents]

    async def update_document_status(
        self,
        db_session: AsyncSession,
        unique_identifier: UUID,
        update_request: UpdateDocRequest,
    ) -> int:
        """
        Update the status of a document.
        This triggers a background task to index the document once
        Document has been uploaded to storage.
        """
        row_count = await self.db_client.update_document_status(
            db_session,
            UpdateOrgFileRecordRequest(
                unique_identifier=unique_identifier,
                status=update_request.status,
            ),
        )
        if row_count and update_request.status == DocumentStatusEnum.UPLOADED:
            process_document.delay(unique_identifier)
        return row_count

    async def semantic_search(
        self, db_session: AsyncSession, input_query: str
    ) -> List[SemanticSearchResponse]:
        """
        Creates embedding of input_query and searches for documents
        """
        embedding = self.embeddings_model.embed_query(input_query)
        results = await self.db_client.document_embedding_lookup(db_session, embedding)
        return [
            SemanticSearchResponse(
                file_name=result.document.file_name,
                content=result.content,
                content_metadata=result.content_metadata,
                page_number=result.page_number,
            )
            for result in results
        ]
