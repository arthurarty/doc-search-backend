from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_file import OrganizationFile
from app.schemas.org_file_db_schemas import (
    CreateOrgFileRecordRequest,
    OrgFileRecordResponse,
)


class OrgFileDatabaseClient:
    """
    This client handles crud operations on the database.
    """

    def __init__(self):
        pass

    async def create(
        self, db_session: AsyncSession, org_file_request: CreateOrgFileRecordRequest
    ) -> OrgFileRecordResponse:
        """
        Create an organization file and persist it in the database
        """
        org_file = OrganizationFile(**org_file_request.model_dump())
        db_session.add(org_file)
        await db_session.commit()
        await db_session.refresh(org_file)
        return OrgFileRecordResponse.model_validate(org_file)

    async def get_by_unique_identifier(
        self, db_session: AsyncSession, unique_identifier: UUID
    ) -> OrgFileRecordResponse | None:
        query = select(OrganizationFile).where(
            OrganizationFile.unique_identifier == unique_identifier,
        )
        result_object = await db_session.execute(query)
        org_file = result_object.scalar_one_or_none()
        if org_file:
            return OrgFileRecordResponse.model_validate(org_file)
        return None

    async def get_org_files(
        self,
        db_session: AsyncSession,
        limit: int,
        skip: int
    ):
        """
        Get org_files ordered in descending order by created_at date.
        """
        query = select(
            OrganizationFile
        ).limit(limit).offset(skip).order_by(OrganizationFile.created_at)
        result_object = await db_session.execute(query)
        org_files = result_object.scalars().all()
        return [OrgFileRecordResponse.model_validate(org_file) for org_file in org_files]
