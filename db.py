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
                {"id": row[0], "username": row[1], "email": row[2]}
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