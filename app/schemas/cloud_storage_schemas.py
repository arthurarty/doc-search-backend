from pydantic import BaseModel


class SignedUrlRequest(BaseModel):
    blob_name: str
    content_type: str
    expiry_time: int


class SignedUrlResponse(BaseModel):
    signed_url: str
    blob_name: str
