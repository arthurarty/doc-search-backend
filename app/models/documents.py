import enum
from datetime import datetime
from typing import List
from uuid import UUID, uuid7

from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum, Float, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DocumentStatusEnum(enum.Enum):
    QUEUED_FOR_UPLOAD = "queued_for_upload"
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    UPLOAD_FAILED = "upload_failed"
    INDEXING = "indexing"
    INDEXED = "indexed"
    INDEXING_FAILED = "indexing_failed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_identifier: Mapped[UUID] = mapped_column(
        default=uuid7, index=True, unique=True
    )
    file_name: Mapped[str] = mapped_column(index=True)
    file_size: Mapped[float] = mapped_column(Float)
    content_type: Mapped[str] = mapped_column()
    status: Mapped[DocumentStatusEnum] = mapped_column(
        Enum(DocumentStatusEnum), default=DocumentStatusEnum.UPLOADING
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    embeddings: Mapped[List["DocumentEmbedding"]] = relationship(
        back_populates="document"
    )

    def __repr__(self) -> str:
        return f"Doc(id={self.id}) - {self.file_name}"


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "page_number",
            name="uq_document_embeddings_document_id_page_number",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    page_number: Mapped[int] = mapped_column()
    document: Mapped["Document"] = relationship(back_populates="embeddings")
    content_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    content: Mapped[str] = mapped_column()
    embedding: Mapped[list] = mapped_column(Vector(768))
