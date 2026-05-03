from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateOrgFileRecordRequest(BaseModel):
    """
    Used when creating a database record.
    """

    file_name: str
    unique_identifier: UUID


class CreateOrgFileRecordResponse(BaseModel):
    """
    Response from creating the database record
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    file_name: str
    unique_identifier: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
