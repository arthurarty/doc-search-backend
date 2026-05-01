from app.services.cloud_storage_service import CloudStorageService
from app.services.service_instances import cloud_storage_service
from typing import Annotated
from fastapi import Depends


def get_cloud_storage_service() -> CloudStorageService:
    return cloud_storage_service

CloudStorageServiceDep = Annotated[CloudStorageService, Depends(get_cloud_storage_service)]
