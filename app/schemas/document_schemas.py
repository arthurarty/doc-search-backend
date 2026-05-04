"""
These schemas are user facing, i.e are exposed through the API.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.documents import DocumentStatusEnum


class CreateDocRequest(BaseModel):
    file_name: str
    content_type: str
    file_size: float


class CreateDocResponse(BaseModel):
    signed_url: str
    blob_name: str
    unique_identifier: UUID


class UpdateDocRequest(BaseModel):

    status: DocumentStatusEnum


class DocResponse(BaseModel):
    """
    Response from creating the database record
    """

    model_config = ConfigDict(from_attributes=True, extra="ignore")
    file_name: str
    unique_identifier: UUID
    file_size: float
    content_type: str
    status: DocumentStatusEnum
    created_at: datetime
    updated_at: datetime
