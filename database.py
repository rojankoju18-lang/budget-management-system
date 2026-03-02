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
        # Config for main dashboard cards - now with user tracking
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS config 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_email TEXT, key TEXT, value TEXT, 
                             UNIQUE(user_email, key))""")
        
        # Combined transactions table - now with user tracking
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tx 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_email TEXT, type TEXT, amount REAL, 
                             category TEXT, date TEXT, month TEXT)""")
        self.conn.commit()

    def migrate_tables(self):
        """Migrate existing tables to add user_email column if it doesn't exist"""
        try:
            # Check if config table exists and has proper structure
            self.cursor.execute("PRAGMA table_info(config)")
            config_columns = [col[1] for col in self.cursor.fetchall()]
            
            # Check if tx table exists and has proper structure
            self.cursor.execute("PRAGMA table_info(tx)")
            tx_columns = [col[1] for col in self.cursor.fetchall()]
            
            # If tables don't have user_email, we need to clean them up
            if config_columns and 'user_email' not in config_columns:
                # Drop old tables and recreate with proper schema
                try:
                    self.cursor.execute("DROP TABLE IF EXISTS config")
                    self.cursor.execute("DROP TABLE IF EXISTS tx")
                    self.conn.commit()
                    # Recreate with proper schema
                    self.create_tables()
                except sqlite3.OperationalError:
                    pass
                    
            if tx_columns and 'user_email' not in tx_columns:
                try:
                    self.cursor.execute("DROP TABLE IF EXISTS tx")
                    self.conn.commit()
                    # Recreate with proper schema
                    self.create_tables()
                except sqlite3.OperationalError:
                    pass
                    
        except Exception as e:
            print(f"Migration info: {str(e)}")

    def init_user_config(self, user_email):
        """Initialize default config values for a new user"""
        defaults = {'balance': '0', 'savings': '0', 'remaining_balance': '0', 'day': '1'}
        for k, v in defaults.items():
            self.cursor.execute(
                "INSERT OR IGNORE INTO config (user_email, key, value) VALUES (?, ?, ?)", 
                (user_email, k, v)
            )
        self.conn.commit()

    def get_config(self, user_email, key):
        self.cursor.execute(
            "SELECT value FROM config WHERE user_email=? AND key=?", 
            (user_email, key)
        )
        res = self.cursor.fetchone()
        return float(res[0]) if res else 0.0

    def add_transaction(self, user_email, t_type, amt, cat, date_str):
        # Ensure user config exists
        self.init_user_config(user_email)
        
        # Extract month name for report grouping
        dt = datetime.strptime(date_str, "%Y/%m/%d")
        month_name = dt.strftime("%B")
        
        self.cursor.execute(
            "INSERT INTO tx (user_email, type, amount, category, date, month) VALUES (?,?,?,?,?,?)",
            (user_email, t_type, amt, cat, date_str, month_name)
        )
        
        if t_type == "Income":
            new_bal = self.get_config(user_email, 'balance') + amt
            new_rem = self.get_config(user_email, 'remaining_balance') + amt
            self.cursor.execute(
                "UPDATE config SET value=? WHERE user_email=? AND key=?", 
                (str(new_bal), user_email, 'balance')
            )
            self.cursor.execute(
                "UPDATE config SET value=? WHERE user_email=? AND key=?", 
                (str(new_rem), user_email, 'remaining_balance')
            )
        else:
            new_rem = self.get_config(user_email, 'remaining_balance') - amt
            self.cursor.execute(
                "UPDATE config SET value=? WHERE user_email=? AND key=?", 
                (str(new_rem), user_email, 'remaining_balance')
            )
            if cat == "Savings":
                new_sav = self.get_config(user_email, 'savings') + amt
                self.cursor.execute(
                    "UPDATE config SET value=? WHERE user_email=? AND key=?", 
                    (str(new_sav), user_email, 'savings')
                )
        
        self.conn.commit()

    def get_monthly_sums(self, user_email):
        self.cursor.execute(
            "SELECT month, SUM(amount) FROM tx WHERE user_email=? AND type='Expense' GROUP BY month",
            (user_email,)
        )
        return dict(self.cursor.fetchall())

    def get_category_sums(self, user_email):
        self.cursor.execute(
            "SELECT category, SUM(amount) FROM tx WHERE user_email=? AND type='Expense' GROUP BY category",
            (user_email,)
        )
        return dict(self.cursor.fetchall())
    
    def get_user_transactions(self, user_email):
        """Get all transactions for a specific user"""
        self.cursor.execute(
            "SELECT id, type, category, amount, date FROM tx WHERE user_email=? ORDER BY date DESC",
            (user_email,)
        )
        return self.cursor.fetchall()
    
    def get_user_totals(self, user_email):
        """Get income and expense totals for a user"""
        self.cursor.execute(
            "SELECT type, SUM(amount) FROM tx WHERE user_email=? GROUP BY type",
            (user_email,)
        )
        result = dict(self.cursor.fetchall())
        income = result.get("Income", 0.0)
        expense = result.get("Expense", 0.0)
        return income, expense
    
    def recalculate_user_stats(self, user_email):
        """Recalculate and update user stats from transactions"""
        self.cursor.execute(
            "SELECT type, SUM(amount) FROM tx WHERE user_email=? GROUP BY type",
            (user_email,)
        )
        result = dict(self.cursor.fetchall())
        
        total_income = result.get("Income", 0.0)
        total_expense = result.get("Expense", 0.0)
        
        # Calculate totals
        remaining_balance = total_income - total_expense
        
        # Calculate savings (expenses categorized as Savings)
        self.cursor.execute(
            "SELECT SUM(amount) FROM tx WHERE user_email=? AND type='Expense' AND category='Savings'",
            (user_email,)
        )
        savings_result = self.cursor.fetchone()
        total_savings = savings_result[0] if savings_result[0] else 0.0
        
        # Update config with calculated values
        self.init_user_config(user_email)
        self.cursor.execute(
            "UPDATE config SET value=? WHERE user_email=? AND key=?",
            (str(total_income), user_email, 'balance')
        )
        self.cursor.execute(
            "UPDATE config SET value=? WHERE user_email=? AND key=?",
            (str(remaining_balance), user_email, 'remaining_balance')
        )
        self.cursor.execute(
            "UPDATE config SET value=? WHERE user_email=? AND key=?",
            (str(total_savings), user_email, 'savings')
        )
        self.conn.commit()

db = Database()