from typing import List
from fastapi import UploadFile, HTTPException
import docx2txt
import fitz  # PyMuPDF for PDF
import os
from sentence_transformers import SentenceTransformer
from uuid import UUID
from app.config import db


class Upload:
    """
    Service class for handling document ingestion, embedding, and retrieval.

    This class provides methods to:
    - Extract text from uploaded files (PDF, DOCX, TXT).
    - Split long text into smaller overlapping chunks for efficient embedding.
    - Generate vector embeddings using a SentenceTransformer model
      (default: all-MiniLM-L6-v2, 384 dimensions).
    - Store (upsert) document chunks and embeddings in MongoDB, linked to a
      document ID.
    - Query stored documents using MongoDB Atlas Vector Search to
      retrieve the most relevant chunks based on semantic similarity.

    MongoDB requirements:
    - A vector index (e.g., "vector_index") must be 
      created on the `embedding` field
      with dimensions = 384 and similarity metric (cosine/dotProduct/euclidean).
    - A filter field (e.g., "document_id") should also be indexed to enable
      filtering queries by document.

    Usage:
    - Upload a document → extract & chunk → embed → upsert into MongoDB.
    - Run a query against a document_id → embed query → retrieve top-k 
      relevant chunks via $vectorSearch pipeline.
    """

    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.document_data = db.document_data
        self.document_data.create_index("document_id")
        self.document_data.create_index("chunk_id")

    def extract_text_from_file(self, file: UploadFile) -> str:
        """Extract text from PDF, DOCX, or TXT file."""
        try:
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                buffer.write(file.file.read())

            text = ""
            if file.filename.endswith(".pdf"):
                doc = fitz.open(temp_path)
                for page in doc:
                    text += page.get_text()
                doc.close()

            elif file.filename.endswith(".docx"):
                text = docx2txt.process(temp_path)

            elif file.filename.endswith(".txt"):
                with open(temp_path, "r", encoding="utf-8") as f:
                    text = f.read()

            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format"
                )

            os.remove(temp_path)
            return text.strip()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error reading file: {str(e)}"
            )

    async def extarct_text(self, file):
        text_content = self.extract_text_from_file(file)
        return text_content

    async def chunk_text(
            self,
            text: str,
            chunk_size: int = 5,
            overlap: int = 0
    ) -> List[str]:
        """
        Split long text into smaller overlapping chunks.

        Args:
            text (str): Input text to split
            chunk_size (int): Max length of each chunk
            overlap (int): Number of overlapping characters between chunks

        Returns:
            List[str]: List of text chunks
        """
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            print(chunk, "cuurent chunk \n\n\n\n\n\n")
            chunks.append(chunk.strip())
            start = end - overlap

        return chunks

    async def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """Generate embeddings for chunks."""
        if not chunks:
            return []

        embeddings = self.embedding_model.encode(
            chunks,
            convert_to_numpy=True).tolist()
        return embeddings

    async def upsert_embeddings(
        self,
        document_id: UUID,
        chunks: List[str],
        embeddings: List[List[float]]
    ) -> None:
        """
        Store chunks + embeddings in MongoDB, linked to a document ID.
        Each chunk is stored as a separate record for retrieval.
        """
        try:
            docs = []
            for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                docs.append({
                    "document_id": str(document_id),
                    "chunk_id": idx,
                    "text": chunk,
                    "embedding": emb
                })

            # Remove old entries for this document (if any)
            self.document_data.delete_many({"document_id": str(document_id)})

            # Insert new chunks
            if docs:
                self.document_data.insert_many(docs)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error upserting embeddings: {str(e)}"
            )

    async def query_document(self, document_id: UUID, query: str):
        """
        Query stored document chunks using MongoDB Atlas Vector Search.
        """
        try:
            # 1. Generate embedding for the query
            query_embedding = self.embedding_model.encode(
                query,
                convert_to_numpy=True).tolist()

            # 2. Build pipeline
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 100,
                        "limit": 5,
                        "filter": {
                            "document_id": str(document_id)
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "chunk_id": 1,
                        "text": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]

            # 3. Run aggregation
            cursor = self.document_data.aggregate(pipeline)
            results = await cursor.to_list(length=5)

            if not results:
                raise HTTPException(
                    status_code=404,
                    detail=f"No results found for document_id: {document_id}"
                )

            return results

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error querying document: {str(e)}"
            )


upload_service = Upload()
