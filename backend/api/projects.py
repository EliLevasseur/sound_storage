from fastapi import APIRouter, Form, HTTPException
from psycopg.errors import CheckViolation, ForeignKeyViolation, UniqueViolation

from db.projects import add_member, get_current_user, add_project, get_project_members, get_projects, get_user_role

router = APIRouter()


@router.post("/projects/")
def create_project(
    project_name: str = Form(...), session_token: str = Form(...),
    description: str = Form(...), is_private: bool = Form(...)
):
    user_id = get_current_user(session_token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")

    project_id = add_project(project_name, user_id, description, is_private)
    return {"message": "Project added succesfully", "project_id": project_id}


@router.get("/projects/")
def view_projects(session_token: str):
    user_id = get_current_user(session_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return get_projects(user_id)


@router.post("/project_members/")
def member_add(
    project_id: int = Form(...),
    target_user_id: int = Form(...),
    new_role: str = Form(...),
    session_token: str = Form(...)
):
    """user role mey be owner, collaborator, or viewer"""
    acting_user_id = get_current_user(session_token)

    if acting_user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")

    acting_user_role = get_user_role(project_id, acting_user_id)

    if acting_user_role != "owner":
        raise HTTPException(status_code=403, detail="Only the owner can add members")

    try:
        add_member(project_id, target_user_id, new_role)
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="User is already a member of this project")
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="Project or user not found")
    except CheckViolation:
        raise HTTPException(status_code=400, detail="Invalid project role")
    return {"message": "Member added successfully"}


@router.get("/project_members/")
def view_members(session_token: str):
    user_id = get_current_user(session_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return get_project_members(user_id)
