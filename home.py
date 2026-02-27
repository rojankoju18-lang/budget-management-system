import tkinter as tk
import database

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F3E5F5")
        self.db = database.db
        self.cat_colors = {"Rent": "#5C6BC0", "Food": "#FFEE58", "Savings": "#EF5350", 
                           "Groceries": "#AB47BC", "Study": "#F06292", "Bike": "#00E676"}
        self.setup_ui()

    def setup_ui(self):
        # Cards container
        top = tk.Frame(self, bg="#F3E5F5")
        top.pack(pady=20, fill=tk.X, padx=40)

        # Card definitions
        self.create_card(top, "Balance", self.db.get_config('balance'), "#E8F5E9", 0, 0)
        self.create_card(top, "Remaining Balance", self.db.get_config('remaining_balance'), "#E8F5E9", 0, 1)
        self.create_card(top, "Savings", self.db.get_config('savings'), "#FCE4EC", 1, 0)
        self.create_card(top, "Day", int(self.db.get_config('day')), "#F3E5F5", 1, 1)

        # Pie Chart
        self.canvas = tk.Canvas(self, width=300, height=300, bg="#F3E5F5", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=60, pady=20)
        self.draw_pie()

    def create_card(self, parent, title, val, color, r, c):
        f = tk.Frame(parent, bg=color, width=280, height=100, highlightbackground="#CCC", highlightthickness=1)
        f.grid(row=r, column=c, padx=10, pady=10)
        f.pack_propagate(False)
        tk.Label(f, text=title, bg=color, font=("Arial", 10)).pack(anchor="w", padx=15, pady=(10,0))
        tk.Label(f, text=f"Rs. {val:,.0f}" if title != "Day" else val, 
                 bg=color, font=("Arial", 18, "bold")).pack(anchor="w", padx=15)

    def draw_pie(self):
        data = self.db.get_category_sums()
        total = sum(data.values())
        if total == 0:
            self.canvas.create_oval(50, 50, 250, 250, fill="white", outline="#DDD")
            self.canvas.create_text(150, 150, text="No Data")
            return

        angle = 0
        for cat, amt in data.items():
            extent = (amt / total) * 360
            self.canvas.create_arc(50, 50, 250, 250, start=angle, extent=extent, 
                                   fill=self.cat_colors.get(cat, "gray"), outline="white")
            angle += extent

    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        self.setup_ui()