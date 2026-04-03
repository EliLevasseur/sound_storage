from db import add_user, view_users, add_file, view_files, get_file
from fastapi.responses import Response
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Sound Storage API is running"}

@app.get("/users")
def get_users():
    return view_users()

@app.post("/users")
def create_user(username: str = Form(...), email: str = Form(...)):
    add_user(username, email)
    return {"message": "User added successfully"}

@app.post("/files")
async def upload_file(user_id: int = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    add_file(user_id, file.filename, content)
    return {"message": "File uploaded successfully"}

@app.get("/files")
def get_files():
    return view_files()

@app.get("/files/{file_id}")
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