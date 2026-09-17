"""
Celery Worker Configuration for STATWISE Platform (Docker Page 6, 7 & Prompt T).
Handles asynchronous processing of uploaded documents and batch MCQ generation.
Broker: Redis (redis://redis:6379/0 or localhost)
"""

import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "statwise_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300  # 5 minutes maximum for large document processing
)


@celery_app.task(name="tasks.process_document_and_generate_mcqs")
def process_document_and_generate_mcqs(document_id: str, num_questions: int = 5):
    """
    Background worker task to extract text from an uploaded document,
    generate candidate MCQs, and save them as Drafts in the review pipeline.
    """
    from services.mcq_service import mcq_service
    from services.upload_service import upload_service

    doc_meta = upload_service.documents_metadata.get(document_id)
    if not doc_meta:
        return {"status": "ERROR", "message": f"Document {document_id} not found."}

    stored_path = doc_meta.get("stored_path")
    extracted_text = ""
    if stored_path and os.path.exists(stored_path):
        with open(stored_path, "rb") as f:
            content = f.read()
        if stored_path.lower().endswith(".pdf"):
            extracted_text = mcq_service.extract_text_from_pdf(content)
        else:
            extracted_text = content.decode("utf-8", errors="ignore")

    assessment = mcq_service.generate_mcqs(
        document_text=extracted_text,
        filename=doc_meta.get("filename", "Uploaded_Document.pdf"),
        num_questions=num_questions,
        uploader_id=doc_meta.get("uploader_id", "trainer_dr_sunita")
    )

    doc_meta["processing_status"] = "MCQS_GENERATED_AWAITING_REVIEW"
    return {
        "status": "SUCCESS",
        "document_id": document_id,
        "batch_id": assessment.get("batch_id"),
        "total_generated": assessment.get("total_generated")
    }
