from fastapi import APIRouter
from app.services.google_storage_service import generate_upload_signed_url_v4


router = APIRouter()


@router.get("/signed-url/", tags=["docs"])
async def get_signed_url():
    """
    Get a single signed url.
    How to use the signed url
    "curl -X PUT -H 'Content-Type: application/octet-stream' "
    "--upload-file my-file '<signed_url>'"
    """
    return generate_upload_signed_url_v4()
