import psycopg

def db_connect():
    return psycopg.connect(
        f"dbname=sound_storage user=eli password=nnnn host=192.168.4.63"
        )

def add_user(username: str, email: str):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
                        INSERT INTO users (username, email)
                        VALUES (%s, %s)
                        ''',
                        (username, email)
            )

def view_users():
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
                        SELECT * FROM users
                        ''')
            rows = cur.fetchall()
            for row in rows:
                print(row)