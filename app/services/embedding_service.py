from typing import List
from uuid import UUID

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.db_client import DocumentDbClient
from app.config import settings
from app.database import async_session_maker
from app.logger import logger
from app.models.documents import DocumentStatusEnum
from app.schemas.document_schemas import (
    CreateDocumentEmbeddingRequest,
    SemanticSearchResponse,
    UpdateOrgFileRecordRequest,
)
from app.services.cloud_storage_service import CloudStorageService
from app.utils.file_utils import get_blob_name

TEXT_SPLITTER_CHUNK_SIZE = 500
TEXT_SPLITTER_CHUNK_OVERLAP = 50


class EmbeddingService:
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
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=TEXT_SPLITTER_CHUNK_SIZE,
            chunk_overlap=TEXT_SPLITTER_CHUNK_OVERLAP,
        )

    async def create_document_embeddings(self, document_uuid: UUID):
        """
        Create embeddings for a document and persist them to the database.
        """
        async with async_session_maker() as session:
            document = await self.db_client.get_by_unique_identifier(
                session, unique_identifier=document_uuid
            )
        if not document:
            return None
        if document.status == DocumentStatusEnum.INDEXED:
            logger.info("Document: %s already indexed", document_uuid)
            return None
        blob_path = get_blob_name(document_uuid, document.file_name)
        document_id = document.id
        for i, pdf_page_content in enumerate(
            self.cloud_storage_service.read_blob_contents(blob_path)
        ):
            logger.info("indexing page: %s from document: %s", i, document_id)
            texts = self.text_splitter.split_text(pdf_page_content)
            text_embeddings = []
            for text in texts:
                embedding = self.embeddings_model.embed_query(text)
                text_embeddings.append(
                    CreateDocumentEmbeddingRequest(
                        embedding=embedding,
                        document_id=document_id,
                        page_number=i + 1,
                        content_metadata={},
                        content=text,
                    )
                )
            async with async_session_maker() as session:
                await self.db_client.bulk_create_document_embeddings(
                    session, text_embeddings
                )
        async with async_session_maker() as session:
            await self.db_client.update_document_status(
                session,
                UpdateOrgFileRecordRequest(
                    unique_identifier=document_uuid,
                    status=DocumentStatusEnum.INDEXED,
                ),
            )

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
