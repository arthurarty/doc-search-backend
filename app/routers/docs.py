from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.dependencies import DatabaseSessionDep, DocumentServiceDep
from app.schemas.document_schemas import (
    CreateDocRequest,
    CreateDocResponse,
    DocResponse,
    UpdateDocRequest,
)

router = APIRouter(prefix="/docs")


@router.post(
    "/signed-url/",
    tags=["docs"],
    response_model=CreateDocResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_signed_url(
    file_upload_request: CreateDocRequest,
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
) -> CreateDocResponse:
    """
    Get a single signed url.
    How to use the signed url
    "curl -X PUT -H 'Content-Type: application/octet-stream' "
    "--upload-file my-file '<signed_url>'"
    """
    return await document_service.process_file_upload(db_session, file_upload_request)


@router.get(
    "/{unique_identifier}",
    tags=["docs"],
    response_model=DocResponse | None,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Document not found",
            "content": {
                "application/json": {"example": {"detail": "Document not found"}}
            },
        }
    },
)
async def get_document(
    unique_identifier: UUID,
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
) -> DocResponse | JSONResponse | None:
    """
    Retrieve  a single document from the database.
    """
    response = await document_service.get_document_by_unique_identifier(
        db_session=db_session,
        unique_identifier=unique_identifier,
    )
    if response:
        return response
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Document not found"}
    )


@router.put(
    "/{unique_identifier}",
    tags=["docs"],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Document not found",
            "content": {
                "application/json": {"example": {"detail": "Document not found"}}
            },
        }
    },
)
async def update_document(
    unique_identifier: UUID,
    update_request: UpdateDocRequest,
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
) -> None:
    """
    Update a single document.

    Returns: no content if successful
    """
    row_count = await document_service.update_document_status(
        db_session,
        unique_identifier=unique_identifier,
        update_request=update_request,
    )
    if not row_count:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Document not found"},
        )
    return None


@router.get(
    "/",
    tags=["docs"],
    response_model=List[DocResponse],
    status_code=status.HTTP_200_OK,
)
async def get_documents(
    document_service: DocumentServiceDep,
    db_session: DatabaseSessionDep,
    limit: Annotated[int, Query(le=100)] = 25,
    skip: Annotated[int, Query(ge=0)] = 0,
) -> List[DocResponse]:
    """
    Get documents from the database, ordered in descending order by created_at date
    """
    return await document_service.get_documents(db_session, limit=limit, skip=skip)
