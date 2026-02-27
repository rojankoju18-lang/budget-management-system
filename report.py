import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from report_backend import init_db, get_monthly_expenses, get_expenses_by_category

# make sure database exists
init_db()

# main window
root = tk.Tk()
root.title("Budget Management System - Report")
root.geometry("1000x600")
root.resizable(False, False)

# sidebar navigation
sidebar = tk.Frame(root, bg="#D1A233", width=200, height=600)
sidebar.pack(side="left", fill="y")

menu_items = ["Home", "Report", "Add Income", "Add Expenses", "History", "Setting"]
for item in menu_items:
    tk.Button(sidebar, text=item, bg="#CAAA1E", fg="white",
              relief="flat", width=20, height=2).pack(pady=5)

# main content area
main = tk.Frame(root, bg="white", width=800, height=600)
main.pack(side="right", fill="both", expand=True)

# header
tk.Label(main, text="Monthly Expenses Report",
         font=("Arial", 20, "bold"), bg="white", fg="#1b5e20").pack(pady=10)

# graph button
def show_graph():
    data = get_monthly_expenses()
    if not data:
        messagebox.showinfo("Info", "No expense data yet")
        return
    months = [m for m, _ in data]
    amounts = [a for _, a in data]
    plt.bar(months, amounts, color="#DBA134")
    plt.title("Monthly Expenses Report")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.show()

tk.Button(main, text="Show Graph", command=show_graph,
          bg="green", fg="white", width=20).pack(pady=10)

# expense table
tk.Label(main, text="Expense by Category",
         font=("Arial", 16, "bold"), bg="white").pack(pady=10)

tree = ttk.Treeview(main, columns=("Date", "Month", "Category", "Amount"), show="headings")
tree.pack(fill="both", expand=True, padx=20, pady=10)

for col in ("Date", "Month", "Category", "Amount"):
    tree.heading(col, text=col)

rows = get_expenses_by_category()
for r in rows:
    tree.insert("", tk.END, values=r)

root.mainloop()
