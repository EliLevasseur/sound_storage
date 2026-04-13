from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from db.files import add_file, get_file, view_files
from file_storage import download_file_bytes, save_upload_file

router = APIRouter()


@router.post("/files")
async def upload_file(user_id: int = Form(...), file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file name")

    storage_key, size_bytes = save_upload_file(user_id, file)
    add_file(user_id, file.filename, storage_key, size_bytes)
    return {"message": "File uploaded successfully"}


@router.get("/files")
def get_files():
    return view_files()


@router.get("/files/{file_id}")
def download_file(file_id: int):
    result = get_file(file_id)

    if not result:
        raise HTTPException(status_code=404, detail="File not found")

    file_name, storage_key = result
    file_data = download_file_bytes(storage_key)

    return Response(
        content=file_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
