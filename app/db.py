import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_settings = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def connect_db():
    return psycopg2.connect(**db_settings)