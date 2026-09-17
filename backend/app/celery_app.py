"""
Module alias forwarding to backend.celery_app for Docker worker compatibility.
"""
from celery_app import celery_app, process_document_and_generate_mcqs
