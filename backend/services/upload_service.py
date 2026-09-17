"""
Secure Document Upload Service for STATWISE Platform (Prompt J).
Features:
- Multi-format support: PDF, PPTX, DOCX, TXT, and transcript text.
- Server-side extension and MIME-type validation.
- File-size limit enforcement (MAX_UPLOAD_MB from environment or 20MB).
- Strict path sanitization against directory traversal and malicious filenames.
- SHA-256 cryptographic hashing and unique UUID storage IDs.
- Metadata persistence: uploader, hash, source type, access level, processing status.
- Role-based file access controls (only uploader, authorized trainers, and admins).
- Local-volume storage (/app/uploads or ./uploads).
"""

import os
import re
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, UploadFile

# Allowed formats and MIME types
ALLOWED_EXTENSIONS = {".pdf", ".pptx", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "application/octet-stream"  # Fallback for some windows clients
}

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "20"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads"))


def sanitize_filename(filename: str) -> str:
    """Removes path traversals, special characters, and forces safe base naming."""
    base = os.path.basename(filename)
    # Remove null bytes, slashes, backslashes
    clean = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", base)
    if not clean or clean.startswith("."):
        clean = f"document_{uuid.uuid4().hex[:8]}.dat"
    return clean


class DocumentUploadService:
    def __init__(self, storage_dir: str = UPLOAD_DIR):
        self.storage_dir = os.path.abspath(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)
        self.documents_metadata: Dict[str, Dict[str, Any]] = {}
        self._init_seed_documents()

    def _init_seed_documents(self):
        """Seed 3 official verified MoSPI reference documents (Prompt S)."""
        docs = [
            {
                "document_id": "doc_plfs_methodology_2024",
                "filename": "PLFS_Annual_Methodology_Manual_2024.pdf",
                "uploader_id": "trainer_dr_sunita",
                "uploader_role": "TRAINER",
                "source_type": "PDF",
                "file_size_kb": 3840,
                "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "access_level": "RESTRICTED_TRAINING",
                "processing_status": "PROCESSED",
                "pages_count": 84,
                "title": "Periodic Labour Force Survey (PLFS) Sampling & Field Manual",
                "uploaded_at": "2026-03-10T10:00:00Z"
            },
            {
                "document_id": "doc_nas_sources_methods_2024",
                "filename": "NAS_Sources_and_Methods_SNA2008.pdf",
                "uploader_id": "trainer_dr_sunita",
                "uploader_role": "TRAINER",
                "source_type": "PDF",
                "file_size_kb": 5120,
                "file_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
                "access_level": "RESTRICTED_TRAINING",
                "processing_status": "PROCESSED",
                "pages_count": 142,
                "title": "National Accounts Statistics: Sources and Methods (SNA 2008)",
                "uploaded_at": "2026-03-12T14:30:00Z"
            },
            {
                "document_id": "doc_cpi_handbook_2024",
                "filename": "CPI_Methodological_Handbook_Base2012.pdf",
                "uploader_id": "trainer_dr_sunita",
                "uploader_role": "TRAINER",
                "source_type": "PDF",
                "file_size_kb": 2240,
                "file_hash": "b2c3d4e5f6a17890123456789abcdef0123456789abcdef0123456789abcdef1",
                "access_level": "RESTRICTED_TRAINING",
                "processing_status": "PROCESSED",
                "pages_count": 68,
                "title": "Methodological Handbook on Consumer Price Index (Base 2012=100)",
                "uploaded_at": "2026-03-15T09:15:00Z"
            }
        ]
        for d in docs:
            self.documents_metadata[d["document_id"]] = d

    async def save_uploaded_file(
        self,
        file: UploadFile,
        uploader_id: str = "trainer_dr_sunita",
        uploader_role: str = "TRAINER",
        access_level: str = "RESTRICTED_TRAINING"
    ) -> Dict[str, Any]:
        """Validates, hashes, sanitizes, and stores uploaded document."""
        # 1. Check extension
        raw_name = file.filename or "unknown.dat"
        safe_name = sanitize_filename(raw_name)
        _, ext = os.path.splitext(safe_name.lower())

        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # 2. Check MIME type
        if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid MIME type '{file.content_type}' for statistical documents."
            )

        content = await file.read()

        # 3. Check file size
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum allowed size of {MAX_UPLOAD_MB} MB."
            )

        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # 4. Generate unique storage ID and SHA-256 hash
        file_hash = hashlib.sha256(content).hexdigest()
        storage_id = f"doc_{uuid.uuid4().hex[:12]}"
        stored_path = os.path.join(self.storage_dir, f"{storage_id}_{safe_name}")

        with open(stored_path, "wb") as f:
            f.write(content)

        # 5. Determine source type
        source_type = ext.replace(".", "").upper()

        metadata = {
            "document_id": storage_id,
            "filename": safe_name,
            "stored_path": stored_path,
            "uploader_id": uploader_id,
            "uploader_role": uploader_role,
            "source_type": source_type,
            "file_size_kb": round(len(content) / 1024, 1),
            "file_hash": file_hash,
            "access_level": access_level,
            "processing_status": "READY_FOR_EXTRACTION",
            "uploaded_at": datetime.utcnow().isoformat() + "Z"
        }

        self.documents_metadata[storage_id] = metadata
        return metadata

    def verify_file_access(self, document_id: str, user_id: str, user_role: str) -> bool:
        """Enforces access control: only uploader, authorized trainers, and admins may access."""
        doc = self.documents_metadata.get(document_id)
        if not doc:
            return False
        if user_role in ["TRAINER", "ADMIN"]:
            return True
        if doc.get("uploader_id") == user_id:
            return True
        return False

    def list_documents(self, user_role: str = "TRAINER") -> List[Dict[str, Any]]:
        # Sanitized listing excluding internal storage paths
        results = []
        for doc in self.documents_metadata.values():
            item = dict(doc)
            item.pop("stored_path", None)
            results.append(item)
        return results


# Singleton instance
upload_service = DocumentUploadService()
