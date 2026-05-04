"""
These schemas are user facing, i.e are exposed through the API.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.organization_file import FileStatusEnum


class CreateDocRequest(BaseModel):
    file_name: str
    content_type: str
    file_size: float


class UpdateDocRequest(BaseModel):

    status: FileStatusEnum


class DocResponse(BaseModel):
    """
    Response from creating the database record
    """

    model_config = ConfigDict(from_attributes=True, extra="ignore")
    file_name: str
    unique_identifier: UUID
    file_size: float
    content_type: str
    status: FileStatusEnum
    created_at: datetime
    updated_at: datetime
