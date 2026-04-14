import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import UploadFile
from supabase import Client, create_client

load_dotenv(Path(__file__).resolve().parent / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY")
SUPABASE_STORAGE_BUCKET = os.environ["SUPABASE_STORAGE_BUCKET"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def _safe_filename(file_name: str):
    return Path(file_name or "upload.bin").name


def save_upload_file(project_id: int, user_id: int, upload: UploadFile):
    file_name = _safe_filename(upload.filename)
    storage_key = f"projects/{project_id}/{user_id}{uuid4().hex}_{file_name}"


    upload.file.seek(0)
    file_bytes = upload.file.read()
    total_bytes = len(file_bytes)

    supabase.storage.from_(SUPABASE_STORAGE_BUCKET).upload(
        path=storage_key,
        file=file_bytes,
        file_options={
            "content-type": upload.content_type or "application/octet-stream",
            "upsert": "false",
        },
    )

    return storage_key, total_bytes


def download_file_bytes(storage_key: str) -> bytes:
    return supabase.storage.from_(SUPABASE_STORAGE_BUCKET).download(storage_key)
