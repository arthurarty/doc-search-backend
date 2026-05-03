from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OrganizationFile(Base):
    __tablename__ = "organization_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_identifier: Mapped[UUID] = mapped_column(
        default=uuid4, index=True, unique=True
    )
    file_name: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None]

    def __repr__(self) -> str:
        return f"OrgFile(id={self.id}) - {self.file_name}"
