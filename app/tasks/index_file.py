"""
Read a file from GCP and create vector embeddings.
"""

from uuid import UUID

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.service_instances import cloud_storage_service


def process_file(blob_path: str, file_name: str, unique_identifier: UUID):
    for i, pdf_page_content in enumerate(
        cloud_storage_service.read_blob_contents(blob_path)
    ):
        print(f"indexing file: {i}")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_text(pdf_page_content)
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
