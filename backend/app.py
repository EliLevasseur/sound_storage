from fastapi import FastAPI

from api.files import router as files_router
from api.projects import router as projects_router
from api.users import router as users_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Sound Storage API is running"}

app.include_router(users_router)
app.include_router(files_router)
app.include_router(projects_router)
