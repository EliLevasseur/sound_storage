from db import add_file, add_project, add_user, get_file, get_projects, view_files, view_users
from fastapi.responses import Response
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Sound Storage API is running"}

# -------------------------- USERS -------------------------- 

@app.get("/users")
def get_users():
    return view_users()

@app.post("/users")
def create_user(username: str = Form(...), email: str = Form(...)):
    add_user(username, email)
    return {"message": "User added successfully"}

# -------------------------- FILES -------------------------- 

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

# -------------------------- PROJECTS -------------------------- 
@app.post("/projects/")
def create_project(project_name: str = Form(...), owner_id: int = Form(...), is_private: bool = Form(...)):
    add_project(project_name, owner_id, is_private)
    return {"message": "Project added succesfully"}

@app.get("/projects/")
def view_projects():
    return get_projects()
