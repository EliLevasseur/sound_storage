from db.connection import db_connect


def add_file(user_id: int, file_name: str, storage_key: str, size_bytes: int):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO files (user_id, file_name, storage_key, size_bytes)
                VALUES (%s, %s, %s, %s)
                ''',
                (user_id, file_name, storage_key, size_bytes)
            )


def view_files():
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, user_id, file_name, storage_key FROM files")
            rows = cur.fetchall()
            return [
                {"id": row[0], "user_id": row[1], "file_name": row[2], "storage_key": row[3]}
                for row in rows
            ]


def get_file(file_id: int):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT file_name, storage_key FROM files WHERE id = %s
                ''',
                (file_id,)
            )
            return cur.fetchone()
