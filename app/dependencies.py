from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db_session
from app.services.document_service import DocumentService
from app.services.service_instances import document_service


def get_document_service() -> DocumentService:
    return document_service


DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]
DatabaseSessionDep = Annotated[AsyncSession, Depends(get_async_db_session)]
