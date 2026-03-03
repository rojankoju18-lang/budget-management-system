import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6")
        self.db_path = "signup/users.db"
        self.controller = controller
        self.authenticated_user_id = controller.authenticated_user_id if controller else None
        self.user_data = None
        self.load_user_data()
        self.setup_ui()

    def load_user_data(self):
        """Load user data from signup/users.db"""
        if not self.authenticated_user_id:
            messagebox.showerror("Error", "User not authenticated")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, fullname, email, phone FROM users WHERE id = ?",
                (self.authenticated_user_id,)
            )
            self.user_data = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user data: {str(e)}")

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#F5F0F6")
        header.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(header, text="✏️ Update Profile", font=("Arial", 24, "bold"), bg="#F5F0F6", fg="#4A235A").pack(anchor="w")
        tk.Label(header, text="Update your account information", font=("Arial", 11), bg="#F5F0F6", fg="#666").pack(anchor="w")

        # Main Form Card
        card = tk.Frame(self, bg="white", relief=tk.FLAT, bd=0)
        card.pack(fill=tk.BOTH, expand=False, padx=40, pady=20)
        
        # Add border effect
        border = tk.Frame(card, bg="#8E44AD", height=2)
        border.pack(fill=tk.X)

        form = tk.Frame(card, bg="white")
        form.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Full Name Field
        tk.Label(form, text="Full Name", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_fullname = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        if self.user_data:
            self.entry_fullname.insert(0, self.user_data[1] or "")
        self.entry_fullname.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Email Field
        tk.Label(form, text="Email", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_email = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        if self.user_data:
            self.entry_email.insert(0, self.user_data[2] or "")
        self.entry_email.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Phone Field
        tk.Label(form, text="Phone", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_phone = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        if self.user_data:
            self.entry_phone.insert(0, self.user_data[3] or "")
        self.entry_phone.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Button Frame
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 30))

        tk.Button(btn_frame, text="💾 Save Changes", command=self.save_changes, 
                 bg="#8E44AD", fg="white", font=("Arial", 12, "bold"), 
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=30, pady=10).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="🔒 Logout", command=self.logout_user, 
                 bg="#E74C3C", fg="white", font=("Arial", 12, "bold"), 
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=30, pady=10).pack(side=tk.LEFT, padx=5)

    def save_changes(self):
        """Save updated user information"""
        fullname = self.entry_fullname.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()

        # Validation
        if not fullname:
            messagebox.showerror("Error", "Full name is required")
            return

        if not email:
            messagebox.showerror("Error", "Email is required")
            return

        if not phone:
            messagebox.showerror("Error", "Phone is required")
            return

        # Check if email is unique (if changed)
        if email != self.authenticated_email:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                    conn.close()
                    messagebox.showerror("Error", "Email already exists")
                    return
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check email: {str(e)}")
                return

        # Update user data in database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET fullname = ?, email = ?, phone = ? WHERE id = ?",
                (fullname, email, phone, self.authenticated_user_id)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "✓ Profile updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

    def logout_user(self):
        """Logout and return to authentication"""
        if self.controller:
            self.controller.logout()

    def refresh(self):
        """Refresh the page when shown"""
        # Reload user data and rebuild UI
        for w in self.winfo_children():
            w.destroy()
        self.load_user_data()
        self.setup_ui()
