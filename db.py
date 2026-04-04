import psycopg
from db_connect import db_connect

def add_user(username: str, email: str):
    """Adds a user to the users table in the database"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO users (username, email)
                        VALUES (%s, %s)
                        ''',
                        (username, email)
            )

def view_users():
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT * FROM users
                        ''')
            rows = cur.fetchall()
            return [
                {"id": row[0], "username": row[1], "email": row[2], "date_joined": str(row[3])[:10]}
                for row in rows
            ]

def add_file(user_id: int, file_name: str, file_data: bytes):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO files (user_id, file_name, file_data)
                VALUES (%s, %s, %s)
                ''',
                (user_id, file_name, file_data)
            )

def view_files():
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, user_id, file_name FROM files")
            rows = cur.fetchall()
            return [
                {"id": row[0], "user_id": row[1], "file_name": row[2]}
                for row in rows
            ]

def get_file(file_id: int):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT file_name, file_data FROM files WHERE id = %s
                ''',
                (file_id,)
            )
            return cur.fetchone()
        
def add_project(project_name: str, owner_id: int, is_private: bool):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO projects (project_name, owner_id, is_private)
                VALUES (%s, %s, %s)
                """,
                (project_name, owner_id, is_private)
            )


def get_projects():
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT * FROM projects
                """
            )
            rows = curr.fetchall()
            return [
                {"id": row[0], "owner_id": row[1], "project_name": row[2], "description": row[3], "is_private": row[4], "date_created": row[5]}
                for row in rows
            ]
