<<<<<<< HEAD
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
=======
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
>>>>>>> 9d431f1ab5dccf4c25302d4bd7c5adf2ac7dbf04
        return "Email already exists"