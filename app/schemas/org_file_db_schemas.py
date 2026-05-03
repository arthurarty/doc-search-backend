from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.organization_file import FileStatusEnum


class CreateOrgFileRecordRequest(BaseModel):
    """
    Used when creating a database record.
    """

    file_name: str
    unique_identifier: UUID
    file_size: float
    content_type: str


class OrgFileRecordResponse(BaseModel):
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
