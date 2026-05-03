from pydantic import BaseModel


class FileUploadRequest(BaseModel):
    file_name: str
    content_type: str
    file_size: float
