import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum, Float, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FileStatusEnum(enum.Enum):
    QUEUED_FOR_UPLOAD = "queued_for_upload"
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    UPLOAD_FAILED = "upload_failed"
    INDEXING = "indexing"
    INDEXED = "indexed"
    INDEXING_FAILED = "indexing_failed"
    FAILED = "failed"


class OrganizationFile(Base):
    __tablename__ = "organization_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_identifier: Mapped[UUID] = mapped_column(
        default=uuid4, index=True, unique=True
    )
    file_name: Mapped[str] = mapped_column(index=True)
    file_size: Mapped[float] = mapped_column(Float)
    content_type: Mapped[str] = mapped_column()
    status: Mapped[FileStatusEnum] = mapped_column(
        Enum(FileStatusEnum), default=FileStatusEnum.UPLOADING
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"OrgFile(id={self.id}) - {self.file_name}"
