"""
Read a file from GCP and create vector embeddings.
"""

import asyncio
from uuid import UUID

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.celery_app import celery_app
from app.config import settings
from app.database import async_session_maker
from app.models.documents import DocumentStatusEnum
from app.schemas.document_schemas import (
    CreateDocumentEmbeddingRequest,
    UpdateOrgFileRecordRequest,
)
from app.utils.file_utils import get_blob_name

TEXT_SPLITTER_CHUNK_SIZE = 500
TEXT_SPLITTER_CHUNK_OVERLAP = 50


@celery_app.task
def process_document(doc_identifier: UUID):
    asyncio.run(_process_document(doc_identifier))


async def _process_document(doc_identifier: UUID):
    """
    Create embeddings for each page of a document and store them in the database.
    """
    from app.services.service_instances import cloud_storage_service, db_client

    async with async_session_maker() as session:
        document = await db_client.get_by_unique_identifier(
            session, unique_identifier=doc_identifier
        )
        if not document:
            return None
    blob_path = get_blob_name(doc_identifier, document.file_name)
    document_id = document.id
    embeddings_model = OllamaEmbeddings(
        model=settings.EMBEDDINGS_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TEXT_SPLITTER_CHUNK_SIZE, chunk_overlap=TEXT_SPLITTER_CHUNK_OVERLAP
    )
    for i, pdf_page_content in enumerate(
        cloud_storage_service.read_blob_contents(blob_path)
    ):
        print(f"indexing page: {i} from document: {document_id}")
        texts = text_splitter.split_text(pdf_page_content)
        text_embeddings = []
        for text in texts:
            embedding = embeddings_model.embed_query(text)
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
            await db_client.bulk_create_document_embeddings(session, text_embeddings)
    async with async_session_maker() as session:
        await db_client.update_document_status(
            session,
            UpdateOrgFileRecordRequest(
                unique_identifier=doc_identifier,
                status=DocumentStatusEnum.INDEXED,
            ),
        )
