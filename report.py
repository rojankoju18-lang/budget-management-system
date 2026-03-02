import tkinter as tk
import math
import database

class ReportPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6", padx=30, pady=20)
        self.db = database.db
        self.controller = controller
        self.authenticated_user_id = controller.authenticated_user_id if controller else None
        
        # Color palette matching main.py
        self.colors = {
            "green_card": "#D5F5E3",
            "pink_card": "#FADBD8",
            "rent": "#5D6D7E",
            "food": "#F4D03F",
            "savings": "#C0392B",
            "groceries": "#8E44AD",
            "study": "#EB70AA",
            "bike": "#2ECC71",
        }
        
        # Stats cards area
        self.stats_frame = tk.Frame(self, bg="#F5F0F6")
        self.stats_frame.pack(fill="x", padx=0, pady=0)
        
        # Bottom area: pie chart + legend
        self.bottom_frame = tk.Frame(self, bg="#F5F0F6", pady=20)
        self.bottom_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.bottom_frame, width=400, height=400, 
                                bg="#F5F0F6", highlightthickness=0)
        self.canvas.pack(side="left")
        
        self.legend_frame = tk.Frame(self.bottom_frame, bg="#F5F0F6")
        self.legend_frame.pack(side="left", padx=50)

    def refresh(self):
        # Clear and rebuild cards
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Recalculate stats from transactions to ensure accuracy
        self.db.recalculate_user_stats(self.authenticated_user_id)
        
        # Get data from database for this user
        income = self.db.get_config(self.authenticated_user_id, 'balance')
        remaining = self.db.get_config(self.authenticated_user_id, 'remaining_balance')
        savings = self.db.get_config(self.authenticated_user_id, 'savings')
        day = int(self.db.get_config(self.authenticated_user_id, 'day'))
        categories = self.db.get_category_sums(self.authenticated_user_id)
        spent = sum(categories.values())
        
        # Create stat cards
        self.create_card("Balance", f"Rs. {income:,.0f}", self.colors["green_card"], 0, 0)
        self.create_card("Remaining Balance", f"Rs. {remaining:,.0f}", self.colors["green_card"], 0, 1)
        self.create_card("Savings", f"Rs. {savings:,.0f}", self.colors["pink_card"], 1, 0)
        self.create_card("Day", day, self.colors["pink_card"], 1, 1)

        # Draw pie chart
        self.canvas.delete("all")
        
        if spent == 0:
            # Placeholder if no expenses exist
            self.canvas.create_oval(60, 60, 340, 340, fill="#E0E0E0", outline="white")
            self.canvas.create_text(200, 200, text="No Data", font=("Arial", 12, "italic"))
        else:
            start = 0
            cx, cy, r = 200, 200, 140
            for cat, val in categories.items():
                if val <= 0:
                    continue
                
                percentage = (val / spent) * 100
                extent = (val / spent) * 360
                color = self.colors.get(cat.lower(), "#DDD")
                
                # Draw Slice
                self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent,
                                       fill=color, outline="white")
                
                # Calculate text position for percentage labels
                mid_angle = math.radians(start + (extent / 2))
                tx = cx + (r * 0.7) * math.cos(mid_angle)
                ty = cy - (r * 0.7) * math.sin(mid_angle)
                
                if percentage > 4:  # Only show text if slice is big enough
                    self.canvas.create_text(tx, ty, text=f"{percentage:.1f}%",
                                           fill="white" if color != "#F4D03F" else "black",
                                           font=("Arial", 10, "bold"))
                
                start += extent
            
            # Inner white circle for "Donut" effect
            self.canvas.create_oval(cx-40, cy-40, cx+40, cy+40, fill="white", outline="white")

        # Rebuild legend - show ALL categories like in riwaj.py
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        
        # All possible categories in fixed order
        all_categories = ["Rent", "Food", "Savings", "Groceries", "Study", "Bike"]
        
        for cat in all_categories:
            color = self.colors.get(cat.lower(), "#DDD")
            tk.Label(self.legend_frame, text=cat, font=("Arial", 11, "bold"),
                     bg=color, fg="white" if color != "#F4D03F" else "black",
                     width=25, pady=8).pack(pady=4)

    def create_card(self, title, val, color, r, c):
        card = tk.Frame(self.stats_frame, bg=color, padx=20, pady=20)
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        self.stats_frame.grid_columnconfigure(c, weight=1)
        tk.Label(card, text=title, bg=color, font=("Arial", 11)).pack(anchor="w")
        tk.Label(card, text=val, bg=color, font=("Arial", 18, "bold")).pack(anchor="w")
