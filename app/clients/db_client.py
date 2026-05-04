from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.documents import Document, DocumentEmbeddings
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

    async def create_document_embedding(
        self,
        db_session: AsyncSession,
        create_embedding_request: CreateDocumentEmbeddingRequest,
    ):
        doc_embedding = DocumentEmbeddings(**create_embedding_request.model_dump())
        db_session.add(doc_embedding)
        await db_session.commit()
        await db_session.refresh(doc_embedding)
        return doc_embedding
