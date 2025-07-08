import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

username = ""
forename = ""
surname = ""
password = ""

# Hash the password
password_hash = generate_password_hash(password)

cur.execute(
    "INSERT INTO users (username, forename, surname, password_hash) VALUES (%s, %s, %s, %s)",
    (username, forename, surname, password_hash)
)
conn.commit()
cur.close()
conn.close()

print("User created!")
