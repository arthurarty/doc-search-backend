from celery import Celery

from app.config import settings

celery_app = Celery(
    "doc_search",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    include=["app.tasks.index_file"],
)
