import os
import psycopg2

def get_db_connection():
  db_url = os.getenv("DATABASE_URL")
  return psycopg2.connect(db_url)
