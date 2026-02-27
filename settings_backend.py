import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        currency TEXT,
        phone TEXT
    )
    """)
    conn.commit()
    conn.close()

def get_profile(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fullname, email, currency, phone FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_profile(user_id, fullname, email, currency, phone):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET fullname = ?, email = ?, currency = ?, phone = ?
            WHERE id = ?
        """, (fullname, email, currency, phone, user_id))
        conn.commit()
        conn.close()
        return "SUCCESS"
    except sqlite3.IntegrityError:
        return "Email already exists"
