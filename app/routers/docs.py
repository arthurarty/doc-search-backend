from fastapi import APIRouter

router = APIRouter()


@router.get("/signed-url/", tags=["docs"])
async def get_signed_url():
    """
    Get a single signed url
    """
    return "https://example.com"
