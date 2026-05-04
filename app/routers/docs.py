from uuid import UUID

from fastapi import APIRouter, Query
from typing import List, Annotated

from app.dependencies import DatabaseSessionDep, DocumentServiceDep
from app.schemas.cloud_storage_schemas import SignedUrlResponse
from app.schemas.file_upload_schemas import FileUploadRequest
from app.schemas.org_file_db_schemas import OrgFileRecordResponse

router = APIRouter(prefix="/docs")


@router.post("/signed-url/", tags=["docs"], response_model=SignedUrlResponse)
async def create_signed_url(
    file_upload_request: FileUploadRequest,
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
) -> SignedUrlResponse:
    """
    Get a single signed url.
    How to use the signed url
    "curl -X PUT -H 'Content-Type: application/octet-stream' "
    "--upload-file my-file '<signed_url>'"
    """
    return await document_service.process_file_upload(db_session, file_upload_request)


@router.get(
    "/{unique_identifier}", tags=["docs"], response_model=OrgFileRecordResponse | None
)
async def get_document_by_uuid(
    unique_identifier: UUID,
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
) -> OrgFileRecordResponse | None:
    """
    Retrieve  a single document from the database.
    """
    return await document_service.get_org_file_by_unique_identifier(
        db_session=db_session,
        unique_identifier=unique_identifier,
    )

@router.get("/", tags=["docs"], response_model=List[OrgFileRecordResponse])
async def get_documents(
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
    limit: Annotated[int, Query(le=100)] = 25,
    skip: Annotated[int, Query(ge=0)] = 0,
) -> List[OrgFileRecordResponse]:
    """
    Get documents from the database, ordered in descending order by created_at date
    """
    return await document_service.get_org_files(db_session, limit=limit, skip=skip)
