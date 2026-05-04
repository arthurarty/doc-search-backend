from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_file import OrganizationFile
from app.schemas.org_file_db_schemas import (
    CreateOrgFileRecordRequest,
    UpdateOrgFileRecordRequest,
)


class OrgFileDatabaseClient:
    """
    This client handles crud operations on the database.
    """

    def __init__(self):
        pass

    async def create(
        self, db_session: AsyncSession, org_file_request: CreateOrgFileRecordRequest
    ) -> OrganizationFile:
        """
        Create an organization file and persist it in the database
        """
        org_file = OrganizationFile(**org_file_request.model_dump())
        db_session.add(org_file)
        await db_session.commit()
        await db_session.refresh(org_file)
        return org_file

    async def get_by_unique_identifier(
        self, db_session: AsyncSession, unique_identifier: UUID
    ) -> OrganizationFile | None:
        query = select(OrganizationFile).where(
            OrganizationFile.unique_identifier == unique_identifier,
        )
        result_object = await db_session.execute(query)
        return result_object.scalar_one_or_none()

    async def get_org_files(
        self, db_session: AsyncSession, limit: int, skip: int
    ) -> List[OrganizationFile]:
        """
        Get org_files ordered in descending order by created_at date.
        """
        query = (
            select(OrganizationFile)
            .limit(limit)
            .offset(skip)
            .order_by(OrganizationFile.created_at)
        )
        result_object = await db_session.execute(query)
        return result_object.scalars().all()

    async def update_org_file_status(
        self,
        db_session: AsyncSession,
        update_org_file_request: UpdateOrgFileRecordRequest,
    ) -> int:
        """
        Updates the status of a document.
        Returns: No of records affected
        """
        query = (
            update(OrganizationFile)
            .where(
                OrganizationFile.unique_identifier
                == update_org_file_request.unique_identifier
            )
            .values(status=update_org_file_request.status)
        )
        result = await db_session.execute(query)
        await db_session.commit()
        return result.rowcount
