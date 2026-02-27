import tkinter as tk
import database

class IncomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        f = tk.Frame(self, bg="#FFF9E1", padx=30, pady=30)
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(f, text="Amount", bg="#FFF9E1").pack(anchor="w")
        self.e1 = tk.Entry(f, width=40); self.e1.pack(pady=5)
        
        tk.Label(f, text="Source", bg="#FFF9E1").pack(anchor="w")
        self.e2 = tk.Entry(f, width=40); self.e2.pack(pady=5)
        
        tk.Label(f, text="Date (YYYY/MM/DD)", bg="#FFF9E1").pack(anchor="w")
        self.e3 = tk.Entry(f, width=40); self.e3.pack(pady=5)
        self.e3.insert(0, "2026/06/07")
        
        tk.Button(f, text="+ Add Income", bg="#4CAF50", fg="white", 
                  command=self.save, relief=tk.FLAT, padx=20).pack(pady=20)

    def save(self):
        database.db.add_transaction("Income", float(self.e1.get()), self.e2.get(), self.e3.get())
        self.e1.delete(0, tk.END)