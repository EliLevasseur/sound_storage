from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import Response

from db.files import add_file, get_file, view_files

router = APIRouter()


@router.post("/files")
async def upload_file(user_id: int = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    add_file(user_id, file.filename, content)
    return {"message": "File uploaded successfully"}


@router.get("/files")
def get_files():
    return view_files()


@router.get("/files/{file_id}")
def download_file(file_id: int):
    result = get_file(file_id)

    if not result:
        return {"error": "File not found"}

    file_name, file_data = result

    return Response(
        content=file_data,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={file_name}"
        }
    )
