from db.connection import db_connect
import secrets
from datetime import datetime, timedelta, timezone

def add_user(username: str, password_hash: str, email: str):
    """Adds a user to the users table in the database"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO users (username, password_hash, email)
                        VALUES (%s, %s, %s)
                        ''',
                        (username, password_hash, email)
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
        
def get_user_info(email: str):
    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                SELECT id, password_hash FROM users WHERE email = %s
                """,
                (email,)
            )
            result = curr.fetchone()
            return {"id": result[0], "hash": result[1] } if result else None
        
def update_session(user_id: int):
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    with db_connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (%s, %s, %s)
                """,
                (user_id, session_token, expires_at)
            )
            
    return session_token