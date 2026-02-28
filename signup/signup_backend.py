import sqlite3
import re

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        phone TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()


def signup_user(fullname, phone, email, password, confirm):
    if not all([fullname, phone, email, password, confirm]):
        return "All fields are required"

    if password != confirm:
        return "Passwords do not match"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format"

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (fullname, phone, email, password) VALUES (?, ?, ?, ?)",
            (fullname, phone, email, password)
        )
        conn.commit()
        conn.close()
        return "SUCCESS"
    except sqlite3.IntegrityError:
        return "Email already exists"
    except Exception as e:
        return str(e) or "An error occurred"