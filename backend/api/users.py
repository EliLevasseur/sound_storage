from fastapi import APIRouter, Form

from db.users import add_user, view_users

router = APIRouter()


@router.get("/users")
def get_users():
    return view_users()


@router.post("/users")
def create_user(username: str = Form(...), email: str = Form(...)):
    add_user(username, email)
    return {"message": "User added successfully"}
