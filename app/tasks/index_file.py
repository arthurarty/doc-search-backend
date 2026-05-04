"""
Read a file from GCP and create vector embeddings.
"""

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.database import async_session_maker
from app.schemas.document_schemas import CreateDocumentEmbeddingRequest
from app.services.service_instances import cloud_storage_service, db_client


async def process_document(blob_path: str, document_id: int):
    """
    Create embeddings for each page of a document and store them in the database.
    """
    for i, pdf_page_content in enumerate(
        cloud_storage_service.read_blob_contents(blob_path)
    ):
        print(f"indexing page: {i} from document: {document_id}")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_text(pdf_page_content)
        embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
        async with async_session_maker() as session:
            for text in texts:
                embedding = embeddings_model.embed_query(text)
                await db_client.create_document_embedding(
                    session,
                    CreateDocumentEmbeddingRequest(
                        embedding=embedding,
                        document_id=document_id,
                        content_metadata={
                            "page_id": i,
                        },
                        content=text,
                    ),
                )
