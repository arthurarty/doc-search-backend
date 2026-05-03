from fastapi import APIRouter

from app.dependencies import DatabaseSessionDep, DocumentServiceDep
from app.schemas.cloud_storage_schemas import SignedUrlResponse
from app.schemas.file_upload_schemas import FileUploadRequest

router = APIRouter()


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
