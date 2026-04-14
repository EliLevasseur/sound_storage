from fastapi import APIRouter, Form
from api.user_auth import hash_gen, hash_verify
from db.users import add_user, view_users, get_user_info, update_session

router = APIRouter()


@router.get("/users")
def get_users():
    return view_users()


@router.post("/users")
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    password_hash = hash_gen(password)
    add_user(username, password_hash, email)
    return {"message": "User added successfully"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user_info = get_user_info(email)

    if user_info is None:
        return {"message": "Login failed"}

    if not hash_verify(password, user_info["hash"]):
        return {"message": "Login failed"}
    
    session_token = update_session(user_info["id"])
    return {
        "message": "Login successful",
        "session_token": session_token
    }