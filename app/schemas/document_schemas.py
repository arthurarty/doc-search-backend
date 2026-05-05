from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.documents import DocumentStatusEnum


# # # # Internal Schemas # # # #
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


class CreateDocumentEmbeddingRequest(BaseModel):
    embedding: list
    document_id: int
    page_number: int
    content_metadata: dict
    content: str


# # # # External schemas used by API endpoints # # # #


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
