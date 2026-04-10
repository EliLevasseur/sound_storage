from db.connection import db_connect


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
