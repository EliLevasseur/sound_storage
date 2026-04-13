import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def db_connect():
    return psycopg.connect(os.getenv("DATABASE_URL"))