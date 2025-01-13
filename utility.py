import os
import sqlite3
from fastapi import UploadFile

# Constants
DB_PATH = "pipelines.db"
UPLOADS_DIR = "uploads"

# Database initialization
def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipelines (
                pdf_name TEXT PRIMARY KEY,
                vectorstore_path TEXT,
                pdf_path TEXT
            )
        """)
        conn.commit()

# Helper functions
def save_pdf(file: UploadFile) -> str:
    """Save the uploaded PDF to the uploads directory."""
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    pdf_path = os.path.join(UPLOADS_DIR, file.filename)
    contents = file.file.read()
    with open(pdf_path, "wb") as f:
        f.write(contents)
    return pdf_path

def store_pipeline_metadata(pdf_name: str, pdf_path: str, vectorstore_path: str):
    """Store pipeline metadata in SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO pipelines (pdf_name, pdf_path, vectorstore_path)
            VALUES (?, ?, ?)
        """, (pdf_name, pdf_path, vectorstore_path))
        conn.commit()

def get_pipeline_metadata(pdf_name: str):
    """Retrieve pipeline metadata from SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pdf_path, vectorstore_path FROM pipelines WHERE pdf_name = ?
        """, (pdf_name,))
        return cursor.fetchone()