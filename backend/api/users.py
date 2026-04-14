from fastapi import APIRouter, Form, HTTPException
from psycopg.errors import UniqueViolation
from api.user_auth import hash_gen, hash_verify
from db.users import add_user, view_users, get_user_info, update_session

router = APIRouter()


@router.get("/users")
def get_users():
    return view_users()


@router.post("/users")
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    password_hash = hash_gen(password)
    try:
        add_user(username, password_hash, email)
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Email already exists")
    return {"message": "User added successfully"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user_info = get_user_info(email)

    if user_info is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not hash_verify(password, user_info["hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    session_token = update_session(user_info["id"])
    return {
        "message": "Login successful",
        "session_token": session_token
    }
