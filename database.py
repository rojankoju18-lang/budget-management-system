import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("budget.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.migrate_tables()  # Migrate existing tables if needed

    def create_tables(self):
        # Config for main dashboard cards - with user_id foreign key
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS config 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, key TEXT, value TEXT, 
                             UNIQUE(user_id, key), FOREIGN KEY(user_id) REFERENCES users(id))""")
        
        # Combined transactions table - with user_id foreign key
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tx 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, type TEXT, amount REAL, 
                             category TEXT, date TEXT, month TEXT, FOREIGN KEY(user_id) REFERENCES users(id))""")
        self.conn.commit()

    def migrate_tables(self):
        """Migrate existing tables to use user_id instead of user_email"""
        try:
            # Check if config table exists and has user_email column
            self.cursor.execute("PRAGMA table_info(config)")
            config_columns = [col[1] for col in self.cursor.fetchall()]
            
            # Check if tx table exists and has user_email column
            self.cursor.execute("PRAGMA table_info(tx)")
            tx_columns = [col[1] for col in self.cursor.fetchall()]
            
            # If tables have user_email, drop and recreate with user_id
            if config_columns and 'user_email' in config_columns:
                try:
                    self.cursor.execute("DROP TABLE IF EXISTS config")
                    self.cursor.execute("DROP TABLE IF EXISTS tx")
                    self.conn.commit()
                    self.create_tables()
                except sqlite3.OperationalError:
                    pass
            
            # If tables don't have proper foreign key structure, recreate
            if config_columns and 'user_id' not in config_columns:
                try:
                    self.cursor.execute("DROP TABLE IF EXISTS config")
                    self.cursor.execute("DROP TABLE IF EXISTS tx")
                    self.conn.commit()
                    self.create_tables()
                except sqlite3.OperationalError:
                    pass
                    
        except Exception as e:
            print(f"Migration info: {str(e)}")

    def get_user_id_from_email(self, email):
        """Get user_id from email (from signup/users.db)"""
        try:
            conn = sqlite3.connect("signup/users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except Exception:
            return None

    def init_user_config(self, user_id):
        """Initialize default config values for a new user"""
        defaults = {'balance': '0', 'savings': '0', 'remaining_balance': '0', 'day': '1'}
        for k, v in defaults.items():
            self.cursor.execute(
                "INSERT OR IGNORE INTO config (user_id, key, value) VALUES (?, ?, ?)", 
                (user_id, k, v)
            )
        self.conn.commit()

    def get_config(self, user_id, key):
        self.cursor.execute(
            "SELECT value FROM config WHERE user_id=? AND key=?", 
            (user_id, key)
        )
        res = self.cursor.fetchone()
        return float(res[0]) if res else 0.0

    def add_transaction(self, user_id, t_type, amt, cat, date_str):
        # Ensure user config exists
        self.init_user_config(user_id)
        
        # Extract month name for report grouping
        dt = datetime.strptime(date_str, "%Y/%m/%d")
        month_name = dt.strftime("%B")
        
        self.cursor.execute(
            "INSERT INTO tx (user_id, type, amount, category, date, month) VALUES (?,?,?,?,?,?)",
            (user_id, t_type, amt, cat, date_str, month_name)
        )
        
        if t_type == "Income":
            new_bal = self.get_config(user_id, 'balance') + amt
            new_rem = self.get_config(user_id, 'remaining_balance') + amt
            self.cursor.execute(
                "UPDATE config SET value=? WHERE user_id=? AND key=?", 
                (str(new_bal), user_id, 'balance')
            )
            self.cursor.execute(
                "UPDATE config SET value=? WHERE user_id=? AND key=?", 
                (str(new_rem), user_id, 'remaining_balance')
            )
        else:
            new_rem = self.get_config(user_id, 'remaining_balance') - amt
            self.cursor.execute(
                "UPDATE config SET value=? WHERE user_id=? AND key=?", 
                (str(new_rem), user_id, 'remaining_balance')
            )
            if cat == "Savings":
                new_sav = self.get_config(user_id, 'savings') + amt
                self.cursor.execute(
                    "UPDATE config SET value=? WHERE user_id=? AND key=?", 
                    (str(new_sav), user_id, 'savings')
                )
        
        self.conn.commit()

    def get_monthly_sums(self, user_id):
        self.cursor.execute(
            "SELECT month, SUM(amount) FROM tx WHERE user_id=? AND type='Expense' GROUP BY month",
            (user_id,)
        )
        return dict(self.cursor.fetchall())

    def get_category_sums(self, user_id):
        self.cursor.execute(
            "SELECT category, SUM(amount) FROM tx WHERE user_id=? AND type='Expense' GROUP BY category",
            (user_id,)
        )
        return dict(self.cursor.fetchall())
    
    def get_user_transactions(self, user_id):
        """Get all transactions for a specific user"""
        self.cursor.execute(
            "SELECT id, type, category, amount, date FROM tx WHERE user_id=? ORDER BY date DESC",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def get_user_totals(self, user_id):
        """Get income and expense totals for a user"""
        self.cursor.execute(
            "SELECT type, SUM(amount) FROM tx WHERE user_id=? GROUP BY type",
            (user_id,)
        )
        result = dict(self.cursor.fetchall())
        income = result.get("Income", 0.0)
        expense = result.get("Expense", 0.0)
        return income, expense
    
    def recalculate_user_stats(self, user_id):
        """Recalculate and update user stats from transactions"""
        self.cursor.execute(
            "SELECT type, SUM(amount) FROM tx WHERE user_id=? GROUP BY type",
            (user_id,)
        )
        result = dict(self.cursor.fetchall())
        
        total_income = result.get("Income", 0.0)
        total_expense = result.get("Expense", 0.0)
        
        # Calculate totals
        remaining_balance = total_income - total_expense
        
        # Calculate savings (expenses categorized as Savings)
        self.cursor.execute(
            "SELECT SUM(amount) FROM tx WHERE user_id=? AND type='Expense' AND category='Savings'",
            (user_id,)
        )
        savings_result = self.cursor.fetchone()
        total_savings = savings_result[0] if savings_result[0] else 0.0
        
        # Update config with calculated values
        self.init_user_config(user_id)
        self.cursor.execute(
            "UPDATE config SET value=? WHERE user_id=? AND key=?",
            (str(total_income), user_id, 'balance')
        )
        self.cursor.execute(
            "UPDATE config SET value=? WHERE user_id=? AND key=?",
            (str(remaining_balance), user_id, 'remaining_balance')
        )
        self.cursor.execute(
            "UPDATE config SET value=? WHERE user_id=? AND key=?",
            (str(total_savings), user_id, 'savings')
        )
        self.conn.commit()

db = Database()