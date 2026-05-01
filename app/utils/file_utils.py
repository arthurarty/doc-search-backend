import os


def get_file_extension(filename: str) -> str:
    """Return the file extension from a filename, without the leading dot."""
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".")
