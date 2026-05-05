import logging

from app.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
