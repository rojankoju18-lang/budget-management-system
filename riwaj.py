import tkinter as tk
import math

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
            "rent": "#5D6D7E", "food": "#F4D03F", "savings": "#C0392B",
            "groceries": "#8E44AD", "study": "#EB70AA", "bike": "#2ECC71"
        }

        # Shared Data State - Defaulted to 0
        self.total_income = 0
        self.expenses = {
            "Rent": 0, "Food": 0, "Savings": 0,
            "Groceries": 0, "Study": 0, "Bike": 0
        }

        self.setup_ui()

    def setup_ui(self):
        # --- Top Header ---
        self.header = tk.Frame(self.root, bg="white", height=70)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        tk.Label(self.header, text="🔔", font=("Arial", 18), bg="white").pack(side="left", padx=20)
        tk.Label(self.header, text="Budget Management System", font=("Arial", 20, "bold"), 
                 fg=self.colors["header"], bg="white").pack(side="left", expand=True)
        tk.Label(self.header, text="👤\nAccount", font=("Arial", 9), bg="white").pack(side="right", padx=20)

        # --- Sidebar ---
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Container for screens
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(side="right", expand=True, fill="both")

        self.create_menu_buttons()
        
        # Initialize the screens
        self.frames = {}
        for F in (HomeScreen, ReportScreen, SettingsScreen):
            page_name = F.__name__
            frame = F(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.show_frame("ReportScreen")

    def logout(self):
        """Close this app window and open the login frontend."""
        # destroy the current root before spawning a new Tk instance
        self.root.destroy()
        try:
            # import inside function so it's executed on demand
            import signup.login_frontend  # noqa: F401
        except Exception:
            # if something goes wrong just exit gracefully
            pass

    def create_menu_buttons(self):
        menu_items = [
            ("🏠 Home", "HomeScreen"),
            ("📊 Report", "ReportScreen"),
            ("➕ Add income", "HomeScreen"),
            ("➕ Add Expenses", "HomeScreen"),
            ("📅 History", "HomeScreen"),
            ("🔒 logout", "logoutScreen")
        ]

        self.nav_buttons = {}
        for text, target in menu_items:
            # logout needs a special handler instead of raising a frame
            if target == "logoutScreen":
                cmd = self.logout
            else:
                cmd = lambda t=target: self.show_frame(t)

            btn = tk.Button(self.sidebar, text=f"  {text}", font=("Arial", 12, "bold"),
                            anchor="w", bg=self.colors["sidebar"], relief="flat", bd=0, 
                            padx=20, pady=15, cursor="hand2",
                            command=cmd)
            btn.pack(fill="x", pady=1)
            self.nav_buttons[target] = btn

    def show_frame(self, page_name):
        for name, btn in self.nav_buttons.items():
            btn.configure(bg=self.colors["sidebar"])
        if page_name in self.nav_buttons:
            self.nav_buttons[page_name].configure(bg=self.colors["active_tab"])
        
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "refresh"): frame.refresh()

# --- Screen: HOME ---
class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F0F6")
        tk.Label(self, text="Welcome Home", font=("Arial", 24, "bold"), bg="#F5F0F6").pack(pady=50)
        tk.Label(self, text="Select 'Report' to see the dashboard", font=("Arial", 12), bg="#F5F0F6").pack()

# --- Screen: REPORT (THE DASHBOARD) ---
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
        
        spent = sum(self.controller.expenses.values())
        rem = self.controller.total_income - spent
        
        self.create_card("Balance", f"Rs. {self.controller.total_income:,}", self.controller.colors["green_card"], 0, 0)
        self.create_card("Remaining Balance", f"Rs. {rem:,}", self.controller.colors["green_card"], 0, 1)
        self.create_card("Savings", f"Rs. {self.controller.expenses['Savings']:,}", self.controller.colors["pink_card"], 1, 0)
        self.create_card("Day", "25", self.controller.colors["pink_card"], 1, 1)

        self.canvas.delete("all")
        
        if spent == 0:
            # Placeholder if no expenses exist
            self.canvas.create_oval(60, 60, 340, 340, fill="#E0E0E0", outline="white")
            self.canvas.create_text(200, 200, text="No Data", font=("Arial", 12, "italic"))
        else:
            start = 0
            cx, cy, r = 200, 200, 140
            for cat, val in self.controller.expenses.items():
                if val <= 0: continue # Skip zero values in drawing
                
                percentage = (val / spent) * 100
                extent = (val / spent) * 360
                color = self.controller.colors.get(cat.lower(), "#DDD")
                
                # Draw Slice
                self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent, fill=color, outline="white")
                
                # Calculate text position for percentage labels
                # We find the middle angle of the slice
                mid_angle = math.radians(start + (extent / 2))
                # Push text slightly outside the center (r * 0.7)
                tx = cx + (r * 0.7) * math.cos(mid_angle)
                ty = cy - (r * 0.7) * math.sin(mid_angle) # Y is inverted in canvas
                
                if percentage > 4: # Only show text if slice is big enough
                    self.canvas.create_text(tx, ty, text=f"{percentage:.1f}%", 
                                           fill="white" if color != "#F4D03F" else "black",
                                           font=("Arial", 10, "bold"))
                
                start += extent
            
            # Inner white circle for "Donut" effect
            self.canvas.create_oval(cx-40, cy-40, cx+40, cy+40, fill="white", outline="white")

        for widget in self.legend_frame.winfo_children(): widget.destroy()
        for cat, val in self.controller.expenses.items():
            color = self.controller.colors.get(cat.lower(), "#DDD")
            tk.Label(self.legend_frame, text=cat, font=("Arial", 11, "bold"), 
                     bg=color, fg="white" if color != "#F4D03F" else "black", 
                     width=25, pady=8).pack(pady=4)

    def create_card(self, title, val, color, r, c):
        card = tk.Frame(self.stats_frame, bg=color, padx=20, pady=20)
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        self.stats_frame.grid_columnconfigure(c, weight=1)
        tk.Label(card, text=title, bg=color, font=("Arial", 11)).pack(anchor="w")
        tk.Label(card, text=val, bg=color, font=("Arial", 18, "bold")).pack(anchor="w")

# --- Screen: SETTINGS (TO UPDATE DATA) ---
class SettingsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white", padx=40, pady=40)
        self.controller = controller
        tk.Label(self, text="Settings / Update Budget", font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 20))

        tk.Label(self, text="Monthly Income:", bg="white").pack(anchor="w")
        self.inc_ent = tk.Entry(self, font=("Arial", 12))
        self.inc_ent.insert(0, str(controller.total_income))
        self.inc_ent.pack(fill="x", pady=5)

        self.entries = {}
        for cat, val in controller.expenses.items():
            tk.Label(self, text=f"{cat} Expense:", bg="white").pack(anchor="w")
            e = tk.Entry(self, font=("Arial", 12))
            e.insert(0, str(val))
            e.pack(fill="x", pady=5)
            self.entries[cat] = e

        tk.Button(self, text="Save Changes", bg="#4A235A", fg="white", pady=10,
                  command=self.save_data).pack(fill="x", pady=20)

    def save_data(self):
        try:
            self.controller.total_income = int(self.inc_ent.get())
            for cat, ent in self.entries.items():
                self.controller.expenses[cat] = int(ent.get())
            self.controller.show_frame("ReportScreen")
        except ValueError:
            # Simple error handling for non-integer inputs
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()