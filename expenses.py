import tkinter as tk
import database

class ExpensesPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#E8F5E9")
        tk.Label(self, text="Choose What you want to track", font=("Arial", 18, "bold"), bg="#E8F5E9").pack(pady=20)
        
        self.amt = tk.Entry(self, font=("Arial", 14)); self.amt.pack(pady=10)
        self.amt.insert(0, "0")

        grid = tk.Frame(self, bg="#E8F5E9")
        grid.pack()
        
        cats = ["Food", "Rent", "Groceries", "Study", "Bike", "Savings", "Bills", "Travel"]
        for i, c in enumerate(cats):
            btn = tk.Button(grid, text=f"{c} +", width=15, pady=8, bg="white", relief=tk.FLAT,
                            command=lambda x=c: self.add(x))
            btn.grid(row=i//2, column=i%2, padx=15, pady=10)

    def add(self, cat):
        database.db.add_transaction("Expense", float(self.amt.get()), cat, "2026/06/07")