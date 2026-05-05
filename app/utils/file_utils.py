import os
from uuid import UUID


def get_file_extension(filename: str) -> str:
    """Return the file extension from a filename, without the leading dot."""
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".")


def get_blob_name(unique_identifier: UUID, file_name: str) -> str:
    """
    Return blob name used to store file
    """
    file_extension = get_file_extension(file_name)
    return f"{unique_identifier.hex}.{file_extension}"
