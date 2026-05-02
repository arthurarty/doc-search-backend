from fastapi import APIRouter

from app.dependencies import CloudStorageServiceDep
from app.schemas.cloud_storage_schemas import FileUploadRequest, SignedUrlResponse

router = APIRouter()


@router.post("/signed-url/", tags=["docs"], response_model=SignedUrlResponse)
async def create_signed_url(
    file_upload_request: FileUploadRequest,
    cloud_storage_service: CloudStorageServiceDep,
) -> SignedUrlResponse:
    """
    Get a single signed url.
    How to use the signed url
    "curl -X PUT -H 'Content-Type: application/octet-stream' "
    "--upload-file my-file '<signed_url>'"
    """
    return cloud_storage_service.create_upload_signed_url(file_upload_request)
