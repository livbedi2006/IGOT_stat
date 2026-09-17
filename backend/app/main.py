"""
Module alias forwarding to backend.main:app for Docker uvicorn compatibility.
"""
import sys
import os

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
