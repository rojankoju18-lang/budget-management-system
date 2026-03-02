import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6")
        self.controller = controller
        tk.Label(self, text="Welcome Home", font=("Arial", 24, "bold"), bg="#F5F0F6").pack(pady=50)
        tk.Label(self, text="Select 'Report' to see the dashboard", font=("Arial", 12), bg="#F5F0F6").pack()
