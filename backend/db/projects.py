from db.connection import db_connect


def add_project(project_name: str, owner_id: int, description: str, is_private: bool):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO projects (project_name, owner_id, description, is_private)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (project_name, owner_id, description, is_private)
            )
            project_id = curr.fetchone()[0]

            curr.execute(
                """
                INSERT INTO project_members (project_id, user_id, user_role)
                VALUES (%s, %s, %s)
                """,
                (project_id, owner_id, "owner")
            )

            return project_id


def get_projects(user_id: int):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT projects.id, projects.owner_id, projects.project_name,
                       projects.description, projects.is_private, projects.created_at
                FROM projects
                INNER JOIN project_members ON projects.id = project_members.project_id
                WHERE project_members.user_id = %s
                ORDER BY projects.created_at DESC
                """,
                (user_id,)
            )
            rows = curr.fetchall()
            return [
                {"id": row[0], "owner_id": row[1], "project_name": row[2], "description": row[3], "is_private": row[4], "date_created": str(row[5])[:10]}
                for row in rows
            ]


def get_project_members(user_id: int):
    """Returns a list of projects alongside their project members"""
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT projects.project_name, users.username, project_members.user_role
                FROM project_members
                INNER JOIN projects ON project_members.project_id = projects.id
                INNER JOIN users ON project_members.user_id = users.id
                WHERE project_members.project_id IN (
                    SELECT project_id
                    FROM project_members
                    WHERE user_id = %s
                )
                ORDER BY projects.project_name, users.username;
                """,
                (user_id,)
            )
            rows = curr.fetchall()
            return [
                {'project_name': row[0], 'username': row[1], 'role': row[2]}
                for row in rows
            ]


def add_member(project_id: int, user_id: int, user_role: str):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO project_members (project_id, user_id, user_role)
                VALUES (%s, %s, %s);
                """,
                (project_id, user_id, user_role)
            )


def get_current_user(session_token: str):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT user_id FROM user_sessions WHERE session_token = %s AND expires_at > NOW()
                """,
                (session_token,)
            )
            result = curr.fetchone()
            return result[0] if result else None


def get_user_role(project_id: int, user_id: int):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT user_role FROM project_members WHERE user_id = %s AND project_id = %s
                """,
                (user_id, project_id,)
            )
            result = curr.fetchone()
            return result[0] if result else None
