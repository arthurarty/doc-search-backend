from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_file import OrganizationFile
from app.schemas.org_file_db_schemas import (
    CreateOrgFileRecordRequest,
    CreateOrgFileRecordResponse,
)


class OrgFileDatabaseClient:
    """
    This client handles crud operations on the database.
    """

    def __init__(self):
        pass

    async def create(
        self, db_session: AsyncSession, org_file_request: CreateOrgFileRecordRequest
    ) -> CreateOrgFileRecordResponse:
        """
        Create an organization file and persist it in the database
        """
        org_file = OrganizationFile(**org_file_request.model_dump())
        db_session.add(org_file)
        await db_session.commit()
        await db_session.refresh(org_file)
        return CreateOrgFileRecordResponse.model_validate(org_file)
