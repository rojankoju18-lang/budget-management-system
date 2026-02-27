import tkinter as tk
from tkinter import messagebox
from settings_backend import init_db, get_profile, update_profile

# setup database
init_db()

# assume demo user_id = 1
USER_ID = 1

root = tk.Tk()
root.title("Budget Management System - Settings")
root.geometry("1000x600")
root.resizable(False, False)

# sidebar navigation
sidebar = tk.Frame(root, bg="#E8A936", width=200, height=600)
sidebar.pack(side="left", fill="y")

menu_items = ["Home", "Report", "Add Income", "Add Expenses", "History", "Setting"]
for item in menu_items:
    tk.Button(sidebar, text=item, bg="#E2A534", fg="white",
              relief="flat", width=20, height=2).pack(pady=5)

# main content area
main = tk.Frame(root, bg="white", width=800, height=600)
main.pack(side="right", fill="both", expand=True)

tk.Label(main, text="Update Profile",
         font=("Arial", 20, "bold"), bg="white", fg="#1b5e20").pack(pady=20)

def create_entry(label, default=""):
    frame = tk.Frame(main, bg="white")
    frame.pack(pady=5, padx=20, anchor="w")
    tk.Label(frame, text=label, font=("Arial", 12), bg="white").pack(side="left", padx=10)
    entry = tk.Entry(frame, width=40)
    entry.insert(0, default)
    entry.pack(side="left")
    return entry

# load existing profile
profile = get_profile(USER_ID)
if profile:
    entry_name = create_entry("User Name:", profile[0])
    entry_email = create_entry("Email:", profile[1])
    entry_currency = create_entry("Currency:", profile[2])
    entry_number = create_entry("Number:", profile[3])
else:
    entry_name = create_entry("User Name:")
    entry_email = create_entry("Email:")
    entry_currency = create_entry("Currency:")
    entry_number = create_entry("Number:")

# save profile
def save_profile():
    result = update_profile(USER_ID,
                            entry_name.get(),
                            entry_email.get(),
                            entry_currency.get(),
                            entry_number.get())
    if result == "SUCCESS":
        messagebox.showinfo("Success", "Profile updated successfully")
    else:
        messagebox.showerror("Error", result)

tk.Button(main, text="Update Profile", command=save_profile,
          bg="green", fg="white", width=20).pack(pady=20)

tk.Button(main, text="Logout", bg="red", fg="white", width=20).pack(side="bottom", pady=20)

root.mainloop()
