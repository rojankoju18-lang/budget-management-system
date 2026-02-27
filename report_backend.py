import sqlite3

def init_db():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,        -- Income or Expense
        category TEXT,    -- Food, Rent, etc.
        amount REAL,
        date TEXT         -- YYYY-MM-DD
    )
    """)
    conn.commit()
    conn.close()

def get_monthly_expenses():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%m', date), SUM(amount)
        FROM history
        WHERE type='Expense'
        GROUP BY strftime('%m', date)
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_expenses_by_category():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, strftime('%m', date), category, amount
        FROM history
        WHERE type='Expense'
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
