import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import database


class ExpensesPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6")
        self.db = database.db
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#F5F0F6")
        header.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(header, text="➕ Add Expenses", font=("Arial", 24, "bold"), bg="#F5F0F6", fg="#4A235A").pack(anchor="w")
        tk.Label(header, text="Track your spending", font=("Arial", 11), bg="#F5F0F6", fg="#666").pack(anchor="w")

        # Main Form Card
        card = tk.Frame(self, bg="white", relief=tk.FLAT, bd=0)
        card.pack(fill=tk.BOTH, expand=False, padx=40, pady=20)
        
        # Add border effect
        border = tk.Frame(card, bg="#FADBD8", height=2)
        border.pack(fill=tk.X)

        form = tk.Frame(card, bg="white")
        form.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Amount Field
        tk.Label(form, text="Amount (Rs.)", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_amount = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        self.entry_amount.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Category Selection with color codes
        tk.Label(form, text="Category", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 10))
        
        self.categories = ["Rent", "Food", "Savings", "Groceries", "Study", "Bike"]
        self.category_colors = {
            "Rent": "#5D6D7E", "Food": "#F4D03F", "Savings": "#C0392B",
            "Groceries": "#8E44AD", "Study": "#EB70AA", "Bike": "#2ECC71"
        }
        
        self.selected_category = tk.StringVar(value=self.categories[0])
        
        # Category buttons frame
        cat_frame = tk.Frame(form, bg="white")
        cat_frame.pack(fill=tk.X, pady=(0, 20))
        
        for cat in self.categories:
            btn = tk.Button(cat_frame, text=cat, font=("Arial", 10, "bold"),
                           bg=self.category_colors[cat],
                           fg="white" if cat != "Food" else "black",
                           relief=tk.FLAT, bd=0, padx=12, pady=8,
                           command=lambda c=cat: self.set_category(c))
            btn.pack(side=tk.LEFT, padx=5)
            if cat == self.categories[0]:
                btn.config(relief=tk.SUNKEN, bd=2)

        # Date Field
        tk.Label(form, text="Date (YYYY/MM/DD)", font=("Arial", 12, "bold"), bg="white", fg="#4A235A").pack(anchor="w", pady=(0, 5))
        self.entry_date = tk.Entry(form, font=("Arial", 12), width=35, relief=tk.FLAT, bg="#F8F8F8", bd=0)
        self.entry_date.insert(0, datetime.now().strftime("%Y/%m/%d"))
        self.entry_date.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Button Frame
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 30))

        tk.Button(btn_frame, text="💾 Save Expense", command=self.save, 
                 bg="#E74C3C", fg="white", font=("Arial", 12, "bold"), 
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=30, pady=10).pack(side=tk.LEFT)

    def set_category(self, category):
        self.selected_category.set(category)

    def save(self):
        amt = self.entry_amount.get().strip()
        cat = self.selected_category.get()
        date = self.entry_date.get().strip()

        try:
            amt_val = float(amt)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        if not cat:
            messagebox.showerror("Error", "Category is required")
            return

        try:
            datetime.strptime(date, "%Y/%m/%d")
        except Exception:
            messagebox.showerror("Error", "Date format must be YYYY/MM/DD")
            return

        self.db.add_transaction("Expense", amt_val, cat, date)
        messagebox.showinfo("Success", "✓ Expense added successfully")

        # reset fields
        self.entry_amount.delete(0, tk.END)
        self.selected_category.set(self.categories[0])
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, datetime.now().strftime("%Y/%m/%d"))
        
        # Rebuild UI to show selected category changes
        for w in self.winfo_children():
            w.destroy()
        self.setup_ui()
        
        # navigate back to Report if controller is available
        if self.controller:
            self.controller.show_page("Report")
