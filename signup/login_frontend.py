import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from login_backend import login_user
import signup_frontend# Import the signup frontend to navigate to it


root = tk.Tk()
root.title("login")
root.geometry("900x500")
root.resizable(False, False)

left_frame = tk.Frame(root, width=550, height=500, bg="white")
left_frame.pack(side="left", fill="both")

# Load image (use script directory so it works when launched from elsewhere)
img_path = os.path.join(os.path.dirname(__file__), "login.png")
signup_image = None
try:
    img = Image.open(img_path)
    img = img.resize((450, 350), Image.LANCZOS)
    login_image = ImageTk.PhotoImage(img)
    img_label = tk.Label(left_frame, image=login_image, bg="white")
    img_label.image = login_image
    img_label.pack(expand=True)
except Exception:
    # If image missing or can't be opened, show a placeholder text
    tk.Label(left_frame, text="No image available", bg="white", fg="#666").pack(expand=True)

# ---------- UI ----------
right = tk.Frame(root, bg="#E6E6E6", width=350)
right.pack(side="right", fill="y")

tk.Label(right, text="login", font=("Arial", 22, "bold"), bg="#E6E6E6").pack(pady=20)

def create_entry(label, hide=False):
    tk.Label(right, text=label, bg="#E6E6E6").pack(anchor="w", padx=30)
    e = tk.Entry(right, show="*" if hide else "", width=30)
    e.pack(padx=30, pady=5)
    return e

entry_email = create_entry("Email")
entry_password = create_entry("Password", True)


# ---------- CONNECT FRONTEND TO BACKEND ----------
def handle_login():
    result = login_user(
        entry_email.get(),
        entry_password.get()
    )

    if result == "SUCCESS":
        messagebox.showinfo("Success", "Login completed")
    else:
        messagebox.showerror("Error", result)


def go_to_signup():
    # remove current widgets if you want to reuse the same window…
    for widget in right.winfo_children():
        widget.destroy()
    root.destroy()
    # …then build the signup UI in it
    signup_frontend.show_signup(root)

tk.Button(
    right,
    text="login",
    command=handle_login,
    bg="#6C7CFF",
    fg="white",
    width=20
).pack(pady=20)

tk.Label(right, text="Don't have an account?", bg="#E6E6E6").pack(pady=10)
tk.Button(
    right,
    text="Signup",
    command=go_to_signup,
    bg="#6C7CFF",
    fg="white",
    width=20
).pack(pady=10)

root.mainloop()