import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import database


class IncomePage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6")
        self.db = database.db
        self.controller = controller
        self.authenticated_user_id = controller.authenticated_user_id if controller else None
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#F5F0F6")
        header.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(header, text="➕ Add Income", font=("Arial", 24, "bold"), bg="#F5F0F6", fg="#4A235A").pack(anchor="w")
        tk.Label(header, text="Record your income sources", font=("Arial", 11), bg="#F5F0F6", fg="#666").pack(anchor="w")

        # Main Form Card
        card = tk.Frame(self, bg="white", relief=tk.FLAT, bd=0)
        card.pack(fill=tk.BOTH, expand=False, padx=40, pady=20)
        
        # Add border effect with frame
        border = tk.Frame(card, bg="#D5F5E3", height=2)
        border.pack(fill=tk.X)

        form = tk.Frame(card, bg="white")
        form.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Amount Field
        tk.Label(form, text="Amount (Rs.)", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_amount = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        self.entry_amount.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Source Field
        tk.Label(form, text="Income Source", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_source = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        self.entry_source.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Date Field
        tk.Label(form, text="Date (YYYY/MM/DD)", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_date = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        self.entry_date.insert(0, datetime.now().strftime("%Y/%m/%d"))
        self.entry_date.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Button Frame
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 30))

        tk.Button(btn_frame, text="💾 Save Income", command=self.save, 
                 bg="#2ECC71", fg="white", font=("Arial", 12, "bold"), 
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=30, pady=10).pack(side=tk.LEFT)

    def save(self):
        amt = self.entry_amount.get().strip()
        src = self.entry_source.get().strip()
        date = self.entry_date.get().strip()

        try:
            amt_val = float(amt)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        if not src:
            messagebox.showerror("Error", "Source is required")
            return

        try:
            datetime.strptime(date, "%Y/%m/%d")
        except Exception:
            messagebox.showerror("Error", "Date format must be YYYY/MM/DD")
            return

        self.db.add_transaction(self.authenticated_user_id, "Income", amt_val, src, date)
        messagebox.showinfo("Success", "✓ Income added successfully")

        # reset fields
        self.entry_amount.delete(0, tk.END)
        self.entry_source.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, datetime.now().strftime("%Y/%m/%d"))
        
        # navigate back to Report if controller is available
        if self.controller:
            self.controller.show_page("Report")
