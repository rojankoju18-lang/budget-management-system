import tkinter as tk
from tkinter import ttk
import database

class ReportPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.db = database.db
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Monthly Expenses Report", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        # Bar Chart
        self.c = tk.Canvas(self, height=200, bg="#FCE4EC", highlightthickness=0)
        self.c.pack(fill=tk.X, padx=40, pady=10)
        
        # Table
        self.tree = ttk.Treeview(self, columns=("Date", "Month", "Category", "Amount"), show="headings")
        for col in ("Date", "Month", "Category", "Amount"): self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

    def refresh(self):
        # Update Table
        for i in self.tree.get_children(): self.tree.delete(i)
        self.db.cursor.execute("SELECT date, month, category, amount FROM tx WHERE type='Expense'")
        for row in self.db.cursor.fetchall():
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], f"Rs. {row[3]:,.0f}"))

        # Update Bar Chart
        self.c.delete("all")
        monthly_data = self.db.get_monthly_sums()
        max_val = max(monthly_data.values()) if monthly_data else 1
        months = ["January", "February", "March", "April", "May", "June"]
        
        for i, m in enumerate(months):
            val = monthly_data.get(m, 0)
            h = (val / max_val) * 150 if val > 0 else 0
            self.c.create_rectangle(50+(i*100), 180-h, 100+(i*100), 180, fill="#5C6BC0")
            self.c.create_text(75+(i*100), 190, text=m[:3])