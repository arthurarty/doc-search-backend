from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.documents import Document, DocumentEmbedding
from app.schemas.document_schemas import (
    CreateDocumentEmbeddingRequest,
    CreateOrgFileRecordRequest,
    UpdateOrgFileRecordRequest,
)


class DocumentDbClient:
    """
    This client handles crud operations on the database.
    """

    def __init__(self):
        pass

    async def create_document(
        self, db_session: AsyncSession, org_file_request: CreateOrgFileRecordRequest
    ) -> Document:
        """
        Create an organization file and persist it in the database
        """
        org_file = Document(**org_file_request.model_dump())
        db_session.add(org_file)
        await db_session.commit()
        await db_session.refresh(org_file)
        return org_file

    async def get_by_unique_identifier(
        self, db_session: AsyncSession, unique_identifier: UUID
    ) -> Document | None:
        query = select(Document).where(
            Document.unique_identifier == unique_identifier,
        )
        result_object = await db_session.execute(query)
        return result_object.scalar_one_or_none()

    async def get_documents(
        self, db_session: AsyncSession, limit: int, skip: int
    ) -> List[Document]:
        """
        Get org_files ordered in descending order by created_at date.
        """
        query = select(Document).limit(limit).offset(skip).order_by(Document.created_at)
        result_object = await db_session.execute(query)
        return result_object.scalars().all()

    async def update_document_status(
        self,
        db_session: AsyncSession,
        update_org_file_request: UpdateOrgFileRecordRequest,
    ) -> int:
        """
        Updates the status of a document.
        Returns: No of records affected
        """
        query = (
            update(Document)
            .where(
                Document.unique_identifier == update_org_file_request.unique_identifier
            )
            .values(status=update_org_file_request.status)
        )
        result = await db_session.execute(query)
        await db_session.commit()
        return result.rowcount

    async def bulk_create_document_embeddings(
        self,
        db_session: AsyncSession,
        embedding_requests: List[CreateDocumentEmbeddingRequest],
    ) -> None:
        """
        Bulk create document embeddings.
        """
        db_session.add_all(
            [DocumentEmbedding(**req.model_dump()) for req in embedding_requests]
        )
        await db_session.commit()

    async def document_embedding_lookup(
        self,
        db_session: AsyncSession,
        search_embedding: list,
        limit: int | None = 5,
        max_distance: float = 0.4,
    ) -> List[DocumentEmbedding]:
        """
        Uses cosine_distance to look up relevant documents.

        Args:
          db_session: Active async database session.
          search_embedding: Vector embedding of the search query.
          limit: Maximum number of results to return (default 5).
          max_distance: Cosine distance threshold; 0 is an exact match, 2 is
            the exact opposite — lower values yield more relevant results
            (default 0.4).

        Returns:
          List of DocumentEmbedding rows ordered by ascending distance.
        """
        distance = DocumentEmbedding.embedding.cosine_distance(search_embedding)
        query = (
            select(DocumentEmbedding)
            .where(distance <= max_distance)
            .order_by(distance)
            .limit(limit)
        )
        result_object = await db_session.execute(query)
        return result_object.scalars().all()
