from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from db.projects import get_current_user, get_user_role
from db.files import add_file, get_file, view_files
from file_storage import download_file_bytes, save_upload_file

router = APIRouter()


@router.post("/files")
async def upload_file(session_token: str = Form(...), file: UploadFile = File(...), project_id: int = Form(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file name")

    user_id = get_current_user(session_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    user_role = get_user_role(project_id, user_id)
    if user_role in ["owner", "collaborator"]:
        storage_key, size_bytes = save_upload_file(project_id, user_id, file)
        add_file(user_id, file.filename, storage_key, size_bytes, project_id)
        return {"message": "File uploaded successfully"}
    raise HTTPException(status_code=403, detail="viewers cannot upload files to the project")


@router.get("/files")
def get_files(project_id: int, session_token: str):
    user_id = get_current_user(session_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")

    user_role = get_user_role(project_id, user_id)

    if user_role is None:
        raise HTTPException(status_code=403, detail="You are not a part of this project")
    
    return view_files(project_id)


@router.get("/files/{file_id}")
def download_file(file_id: int, session_token: str):
    result = get_file(file_id)

    if not result:
        raise HTTPException(status_code=404, detail="File not found")

    file_name, storage_key, project_id = result

    user_id = get_current_user(session_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")

    user_role = get_user_role(project_id, user_id)
    if user_role is None:
        raise HTTPException(status_code=403, detail="You are not a part of this project")

    file_data = download_file_bytes(storage_key)

    return Response(
        content=file_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
