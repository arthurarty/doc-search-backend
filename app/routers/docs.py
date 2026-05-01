from fastapi import APIRouter
from app.dependencies import CloudStorageServiceDep

router = APIRouter()


@router.get("/signed-url/", tags=["docs"])
async def get_signed_url(
    cloud_storage_service: CloudStorageServiceDep
):
    """
    Get a single signed url.
    How to use the signed url
    "curl -X PUT -H 'Content-Type: application/octet-stream' "
    "--upload-file my-file '<signed_url>'"
    """
    return cloud_storage_service.create_upload_signed_url()
