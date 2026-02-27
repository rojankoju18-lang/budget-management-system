import tkinter as tk
from tkinter import font
import home, income, expenses, report

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Management System")
        self.geometry("1100x750")
        self.configure(bg="#F3E5F5") # Light lavender background

        # Navigation State
        self.current_frame = None
        self.pages = {
            "Home": home.HomePage, "Report": report.ReportPage,
            "Add income": income.IncomePage, "Add Expenses": expenses.ExpensesPage
        }

        # UI Layout
        self.header = tk.Frame(self, bg="#4B2F74", height=70)
        self.header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.header, text="Budget Management System", fg="white", 
                 bg="#4B2F74", font=("Arial", 20, "bold")).pack(pady=15)

        self.sidebar = tk.Frame(self, bg="#FFB300", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self, bg="#F3E5F5")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_nav()
        self.show_page("Home")

    def setup_nav(self):
        for name in ["Home", "Report", "Add income", "Add Expenses", "History", "Setting"]:
            btn = tk.Button(self.sidebar, text=name, bg="#FFB300", fg="black", font=("Arial", 12),
                            relief=tk.FLAT, pady=15, anchor="w", padx=20,
                            command=lambda n=name: self.show_page(n))
            btn.pack(fill=tk.X)

    def show_page(self, name):
        if name not in self.pages: return
        if self.current_frame: self.current_frame.destroy()
        
        self.current_frame = self.pages[name](self.content)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        if hasattr(self.current_frame, "refresh"): self.current_frame.refresh()

if __name__ == "__main__":
    BudgetApp().mainloop()