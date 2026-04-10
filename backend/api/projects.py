from fastapi import APIRouter, Form

from db.projects import add_member, add_project, get_project_id, get_project_members, get_projects

router = APIRouter()


@router.post("/projects/")
def create_project(project_name: str = Form(...), owner_id: int = Form(...), is_private: bool = Form(...)):
    add_project(project_name, owner_id, is_private)
    add_member(get_project_id(project_name), owner_id, "owner")
    return {"message": "Project added succesfully"}


@router.get("/projects/")
def view_projects():
    return get_projects()


@router.post("/project_members/")
def member_add(project_id: int = Form(...), user_id: int = Form(...), user_role: str = Form(...)):
    add_member(project_id, user_id, user_role)
    return {"message": "Member added succesfully"}


@router.get("/project_members/")
def view_members():
    return get_project_members()
