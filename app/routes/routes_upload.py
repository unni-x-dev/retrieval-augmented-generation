from uuid import UUID
from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.schema_base import BaseHttpResponse
from app.services.service_upload import upload_service
from fastapi import status

from app.utils.exception import handle_exceptions

router = APIRouter()


@router.post(
    "/extract-text",
    response_model=BaseHttpResponse,
    summary="Extract text from uploaded file"
)
@handle_exceptions
async def extract_text(
    file: UploadFile = File(..., description="Upload a file (PDF, DOCX, TXT)"),
    document_id: UUID = Form(..., description="Unique document identifier (UUID)")
):
    """
    Upload a file (PDF, Word, or TXT) and get its text content.
    """
    text_content = await upload_service.extarct_text(file)
    chunks = await upload_service.chunk_text(
        text_content,
        chunk_size=500,
        overlap=50
    )
    embeddings = await upload_service.embed_chunks(chunks)
    await upload_service.upsert_embeddings(
        document_id=document_id,
        chunks=chunks,
        embeddings=embeddings
    )
    return BaseHttpResponse(
        status=status.HTTP_200_OK,
        message="Work completed",
        data={
            "text": text_content,
            "chunks": chunks,
            "embeddings": embeddings
        }
    )


@router.post(
    "/query-document",
    response_model=BaseHttpResponse,
    summary="Query a document by ID and get top 5 relevant chunks"
)
@handle_exceptions
async def query_document(
    document_id: UUID = Form(
        ..., description="Unique document identifier (UUID)"),
    query: str = Form(..., description="Natural language question/query")
):
    """
    Given a document_id and a query:
    - Generate embedding for the query
    - Retrieve stored chunks + embeddings
    - Compute cosine similarity
    - Return top 5 most relevant chunks
    """
    results = await upload_service.query_document(document_id, query)

    return BaseHttpResponse(
        status=status.HTTP_200_OK,
        message="Top 5 relevant chunks retrieved",
        data={
            "document_id": str(document_id),
            "query": query,
            "results": results
        }
    )
