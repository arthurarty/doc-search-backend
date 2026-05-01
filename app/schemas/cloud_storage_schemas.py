from pydantic import BaseModel


class FileUploadRequest(BaseModel):
    file_name: str
    content_type: str


class SignedUrlResponse(BaseModel):
    signed_url: str
    blob_name: str
