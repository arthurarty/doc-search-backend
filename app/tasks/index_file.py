"""
Read a file from GCP and create vector embeddings.
"""

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.database import async_session_maker
from app.schemas.document_schemas import CreateDocumentEmbeddingRequest
from app.services.service_instances import cloud_storage_service, db_client

TEXT_SPLITTER_CHUNK_SIZE = 500
TEXT_SPLITTER_CHUNK_OVERLAP = 50


async def process_document(blob_path: str, document_id: int):
    """
    Create embeddings for each page of a document and store them in the database.
    """
    embeddings_model = OllamaEmbeddings(model=settings.EMBEDDINGS_MODEL)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TEXT_SPLITTER_CHUNK_SIZE, chunk_overlap=TEXT_SPLITTER_CHUNK_OVERLAP
    )
    for i, pdf_page_content in enumerate(
        cloud_storage_service.read_blob_contents(blob_path)
    ):
        print(f"indexing page: {i} from document: {document_id}")
        texts = text_splitter.split_text(pdf_page_content)
        text_embeddings = []
        for text in texts:
            embedding = embeddings_model.embed_query(text)
            text_embeddings.append(
                CreateDocumentEmbeddingRequest(
                    embedding=embedding,
                    document_id=document_id,
                    page_number=i,
                    content_metadata={},
                    content=text,
                )
            )
        async with async_session_maker() as session:
            await db_client.bulk_create_document_embeddings(session, text_embeddings)
