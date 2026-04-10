from db_connect import db_connect


def get_project_id(project_name: str):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT id FROM projects WHERE project_name = %s
                """,
                (project_name,)
            )
            result = curr.fetchone()
            return result[0] if result else None