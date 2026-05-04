"""
The schemas in this file are not using facing.
i.e they are for internal services only.
"""

from uuid import UUID

from pydantic import BaseModel

from app.models.documents import DocumentStatusEnum


class CreateOrgFileRecordRequest(BaseModel):
    """
    Used when creating a database record.
    """

    file_name: str
    unique_identifier: UUID
    file_size: float
    content_type: str


class UpdateOrgFileRecordRequest(BaseModel):
    """
    Used to update an org file.
    """

    unique_identifier: UUID
    status: DocumentStatusEnum
