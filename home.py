import tkinter as tk
import sqlite3
import os

class HomePage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6")
        self.controller = controller
        self.authenticated_user_email = controller.authenticated_user_email if controller else None
        self.setup_ui()
    
    def setup_ui(self):
        # Fetch user's full name from signup database
        user_name = "User"
        try:
            if self.authenticated_user_email:
                conn = sqlite3.connect("signup/users.db")
                cursor = conn.cursor()
                cursor.execute("SELECT fullname FROM users WHERE email = ?", (self.authenticated_user_email,))
                result = cursor.fetchone()
                if result:
                    user_name = result[0]
                conn.close()
        except Exception:
            pass
        
        # Welcome Frame
        welcome_frame = tk.Frame(self, bg="#F5F0F6")
        welcome_frame.pack(pady=80)
        
        tk.Label(welcome_frame, text=f"Welcome, {user_name}! 👋", font=("Arial", 32, "bold"), 
                 bg="#F5F0F6", fg="#4A235A").pack(pady=20)
        
        tk.Label(welcome_frame, text=f"Email: {self.authenticated_user_email}", font=("Arial", 12), 
                 bg="#F5F0F6", fg="#666").pack(pady=5)
        
        tk.Label(welcome_frame, text="Your personal budget dashboard is ready", font=("Arial", 14), 
                 bg="#F5F0F6", fg="#8E44AD").pack(pady=20)
        
        tk.Label(welcome_frame, text="📊 Select 'Report' to view your dashboard\n💰 Use 'Add Income' and 'Add Expenses' to track transactions\n📅 Check 'History' for all your records", 
                 font=("Arial", 11), bg="#F5F0F6", fg="#666", justify=tk.LEFT).pack(pady=20)
