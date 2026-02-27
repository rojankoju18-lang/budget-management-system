import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("budget.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Config for main dashboard cards
        self.cursor.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
        defaults = {'balance': '0', 'savings': '0', 'remaining_balance': '0', 'day': '1'}
        for k, v in defaults.items():
            self.cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)", (k, v))

        # Combined transactions table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tx 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, amount REAL, 
                             category TEXT, date TEXT, month TEXT)""")
        self.conn.commit()

    def get_config(self, key):
        self.cursor.execute("SELECT value FROM config WHERE key=?", (key,))
        res = self.cursor.fetchone()
        return float(res[0]) if res else 0.0

    def add_transaction(self, t_type, amt, cat, date_str):
        # Extract month name for report grouping
        dt = datetime.strptime(date_str, "%Y/%m/%d")
        month_name = dt.strftime("%B")
        
        self.cursor.execute("INSERT INTO tx (type, amount, category, date, month) VALUES (?,?,?,?,?)",
                            (t_type, amt, cat, date_str, month_name))
        
        if t_type == "Income":
            new_bal = self.get_config('balance') + amt
            new_rem = self.get_config('remaining_balance') + amt
            self.cursor.execute("UPDATE config SET value=? WHERE key='balance'", (str(new_bal),))
            self.cursor.execute("UPDATE config SET value=? WHERE key='remaining_balance'", (str(new_rem),))
        else:
            new_rem = self.get_config('remaining_balance') - amt
            self.cursor.execute("UPDATE config SET value=? WHERE key='remaining_balance'", (str(new_rem),))
            if cat == "Savings":
                new_sav = self.get_config('savings') + amt
                self.cursor.execute("UPDATE config SET value=? WHERE key='savings'", (str(new_sav),))
        
        self.conn.commit()

    def get_monthly_sums(self):
        self.cursor.execute("SELECT month, SUM(amount) FROM tx WHERE type='Expense' GROUP BY month")
        return dict(self.cursor.fetchall())

    def get_category_sums(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM tx WHERE type='Expense' GROUP BY category")
        return dict(self.cursor.fetchall())

db = Database()