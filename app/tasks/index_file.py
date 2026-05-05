"""
Read a file from GCP and create vector embeddings.
"""

import asyncio
from uuid import UUID

from app.celery_app import celery_app


@celery_app.task
def process_document(doc_identifier: UUID):
    asyncio.run(_process_document(doc_identifier))


async def _process_document(doc_identifier: UUID):
    """
    Create embeddings for each page of a document and store them in the database.
    """
    from app.services.service_instances import embedding_service

    await embedding_service.create_document_embeddings(doc_identifier)
