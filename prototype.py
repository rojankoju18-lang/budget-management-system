import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Management System")
        self.root.geometry("1150x750")
        self.root.configure(bg="#F5F0F6")

        # Color Palette
        self.colors = {
            "sidebar": "#FDB913",
            "active_tab": "#FAD7A0",
            "bg": "#F5F0F6",
            "header": "#4A235A",
            "green_card": "#D5F5E3",
            "pink_card": "#FADBD8",
            "table_row_even": "#FDEBD0",
            # Category Colors
            "rent": "#5D6D7E", "food": "#F4D03F", "savings": "#C0392B",
            "groceries": "#8E44AD", "study": "#EB70AA", "bike": "#2ECC71",
            "salary": "#27AE60"
        }

        # Centralized Data Store
        self.transactions = [] 
        
        self.setup_ui()

    def get_totals(self):
        """Calculates income and expense breakdowns from the transaction list."""
        income = sum(float(t['amount'].replace(',', '')) for t in self.transactions if t['type'] == 'Income')
        expenses = { "Rent": 0, "Food": 0, "Savings": 0, "Groceries": 0, "Study": 0, "Bike": 0 }
        
        for t in self.transactions:
            if t['type'] == 'Expense' and t['category'] in expenses:
                expenses[t['category']] += float(t['amount'].replace(',', ''))
        
        total_spent = sum(expenses.values())
        return income, expenses, total_spent

    def setup_ui(self):
        # --- Header ---
        self.header = tk.Frame(self.root, bg="white", height=70)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        tk.Label(self.header, text="Budget Management System", font=("Arial", 20, "bold"), fg=self.colors["header"], bg="white").pack(side="left", expand=True)

        # --- Sidebar ---
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(side="right", expand=True, fill="both")

        self.create_menu_buttons()
        
        self.frames = {}
        for F in (ReportScreen, AddIncomeScreen, AddExpenseScreen, HistoryScreen):
            page_name = F.__name__
            frame = F(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.show_frame("ReportScreen")

    def create_menu_buttons(self):
        menu_items = [
            ("📊 Report", "ReportScreen"),
            ("➕ Add income", "AddIncomeScreen"),
            ("➕ Add Expenses", "AddExpenseScreen"),
            ("📅 History", "HistoryScreen")
        ]
        self.nav_buttons = {}
        for text, target in menu_items:
            btn = tk.Button(self.sidebar, text=f"  {text}", font=("Arial", 12, "bold"), anchor="w", 
                            bg=self.colors["sidebar"], relief="flat", bd=0, padx=20, pady=15, 
                            command=lambda t=target: self.show_frame(t))
            btn.pack(fill="x")
            self.nav_buttons[target] = btn

    def show_frame(self, page_name):
        for name, btn in self.nav_buttons.items():
            btn.configure(bg=self.colors["sidebar"])
        if page_name in self.nav_buttons:
            self.nav_buttons[page_name].configure(bg=self.colors["active_tab"])
        
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "refresh"): frame.refresh()

# --- NEW SCREEN: ADD INCOME ---
class AddIncomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white", padx=50, pady=50)
        self.controller = controller
        tk.Label(self, text="Add income", font=("Arial", 22, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        # Form Container
        form = tk.Frame(self, bg="#FFF8E7", padx=40, pady=40)
        form.pack(fill="x")

        # Fields
        self.amt = self.create_field(form, "Amount", "1,000,000")
        self.src = self.create_field(form, "Source", "Salary")
        self.dte = self.create_field(form, "Date", datetime.now().strftime("%d/%m/%Y"))
        self.dsc = self.create_field(form, "Description", "Monthly Salary Payment")

        # Buttons
        btn_frame = tk.Frame(form, bg="#FFF8E7")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="+ Add Income", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                  padx=20, command=self.save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Clear", bg="white", font=("Arial", 12), padx=20, 
                  command=lambda: [e.delete(0, tk.END) for e in [self.amt, self.src, self.dsc]]).pack(side="left", padx=10)

    def create_field(self, parent, label, default):
        tk.Label(parent, text=label, bg="#FFF8E7", font=("Arial", 11)).pack(anchor="w")
        e = tk.Entry(parent, font=("Arial", 12), bd=0, highlightthickness=1)
        e.insert(0, default)
        e.pack(fill="x", pady=(0, 15), ipady=8)
        return e

    def save(self):
        self.controller.transactions.append({
            "type": "Income", "category": self.src.get(), "amount": self.amt.get(), 
            "date": self.dte.get(), "desc": self.dsc.get()
        })
        self.controller.show_frame("ReportScreen")

# --- NEW SCREEN: ADD EXPENSE ---
class AddExpenseScreen(AddIncomeScreen): # Inherit layout from AddIncome
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.winfo_children()[0].configure(text="Add Expenses")
        self.src_label = [c for c in self.winfo_children()[1].winfo_children() if isinstance(c, tk.Label) and c.cget("text") == "Source"][0]
        self.src_label.configure(text="Category (Rent/Food/Savings/Groceries/Study/Bike)")
        
    def save(self):
        self.controller.transactions.append({
            "type": "Expense", "category": self.src.get(), "amount": self.amt.get(), 
            "date": self.dte.get(), "desc": self.dsc.get()
        })
        self.controller.show_frame("ReportScreen")

# --- UPDATED REPORT SCREEN ---
class ReportScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F0F6", padx=30, pady=20)
        self.controller = controller
        self.stats_frame = tk.Frame(self, bg="#F5F0F6")
        self.stats_frame.pack(fill="x")
        self.bottom_frame = tk.Frame(self, bg="#F5F0F6", pady=20)
        self.bottom_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.bottom_frame, width=400, height=400, bg="#F5F0F6", highlightthickness=0)
        self.canvas.pack(side="left")
        self.legend_frame = tk.Frame(self.bottom_frame, bg="#F5F0F6")
        self.legend_frame.pack(side="left", padx=50)

    def refresh(self):
        for widget in self.stats_frame.winfo_children(): widget.destroy()
        income, expenses, spent = self.controller.get_totals()
        
        self.create_card("Total Income", f"Rs. {income:,.0f}", self.controller.colors["green_card"], 0, 0)
        self.create_card("Remaining Balance", f"Rs. {(income - spent):,.0f}", self.controller.colors["green_card"], 0, 1)
        self.create_card("Savings", f"Rs. {expenses['Savings']:,.0f}", self.controller.colors["pink_card"], 1, 0)
        self.create_card("Total Expenses", f"Rs. {spent:,.0f}", self.controller.colors["pink_card"], 1, 1)

        self.canvas.delete("all")
        if spent == 0:
            self.canvas.create_oval(60, 60, 340, 340, fill="#E0E0E0", outline="white")
        else:
            start, cx, cy, r = 0, 200, 200, 140
            for cat, val in expenses.items():
                if val <= 0: continue
                extent = (val / spent) * 360
                color = self.controller.colors.get(cat.lower(), "#DDD")
                self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent, fill=color, outline="white")
                mid = math.radians(start + (extent / 2))
                self.canvas.create_text(cx+(r*0.7)*math.cos(mid), cy-(r*0.7)*math.sin(mid), text=f"{(val/spent)*100:.1f}%", font=("Arial", 10, "bold"))
                start += extent
            self.canvas.create_oval(cx-40, cy-40, cx+40, cy+40, fill="white", outline="white")

    def create_card(self, title, val, color, r, c):
        card = tk.Frame(self.stats_frame, bg=color, padx=20, pady=20)
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        self.stats_frame.grid_columnconfigure(c, weight=1)
        tk.Label(card, text=title, bg=color, font=("Arial", 11)).pack(anchor="w")
        tk.Label(card, text=val, bg=color, font=("Arial", 18, "bold")).pack(anchor="w")

# --- HISTORY SCREEN ---
class HistoryScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white", padx=30, pady=20)
        self.controller = controller
        tk.Label(self, text="History", font=("Arial", 22, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.tree = ttk.Treeview(self, columns=("Type", "Category", "Amount", "Date"), show='headings')
        for col in ("Type", "Category", "Amount", "Date"): self.tree.heading(col, text=col)
        self.tree.tag_configure('even', background=self.controller.colors["table_row_even"])
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for i, t in enumerate(self.controller.transactions):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=(t['type'], t['category'], t['amount'], t['date']), tags=(tag,))

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
    