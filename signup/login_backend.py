import sqlite3
import re


def login_user(email, password):
    if not all([email, password]):
        return "All fields are required"

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return "SUCCESS"
        else:
            return "Invalid email or password"
    except Exception as e:
        return str(e) or "An error occurred"