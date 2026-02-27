<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from signup_backend import signup_user, init_db

init_db()

root = tk.Tk()
root.title("Signup")
root.geometry("900x500")
root.resizable(False, False)

left_frame = tk.Frame(root, width=550, height=500, bg="white")
left_frame.pack(side="left", fill="both")

# Load image
img = Image.open("Image.png")
img = img.resize((450, 350), Image.LANCZOS)
signup_image = ImageTk.PhotoImage(img)

# ---------- UI ----------
right = tk.Frame(root, bg="#E6E6E6", width=350)
right.pack(side="right", fill="y")

tk.Label(right, text="Signup", font=("Arial", 22, "bold"), bg="#E6E6E6").pack(pady=20)

def create_entry(label, hide=False):
    tk.Label(right, text=label, bg="#E6E6E6").pack(anchor="w", padx=30)
    e = tk.Entry(right, show="*" if hide else "", width=30)
    e.pack(padx=30, pady=5)
    return e

entry_name = create_entry("Full Name")
entry_phone = create_entry("Phone")
entry_email = create_entry("Email")
entry_password = create_entry("Password", True)
entry_confirm = create_entry("Confirm Password", True)


# ---------- CONNECT FRONTEND TO BACKEND ----------
def handle_signup():
    result = signup_user(
        entry_name.get(),
        entry_phone.get(),
        entry_email.get(),
        entry_password.get(),
        entry_confirm.get()
    )

    if result == "SUCCESS":
        messagebox.showinfo("Success", "Signup completed")
    else:
        messagebox.showerror("Error", result)


tk.Button(
    right,
    text="Signup",
    command=handle_signup,
    bg="#6C7CFF",
    fg="white",
    width=20
).pack(pady=20)

=======
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from signup_backend import signup_user, init_db

init_db()

root = tk.Tk()
root.title("Signup")
root.geometry("900x500")
root.resizable(False, False)

left_frame = tk.Frame(root, width=550, height=500, bg="white")
left_frame.pack(side="left", fill="both")

# Load image
img = Image.open("Image.png")
img = img.resize((450, 350), Image.LANCZOS)
signup_image = ImageTk.PhotoImage(img)

# ---------- UI ----------
right = tk.Frame(root, bg="#E6E6E6", width=350)
right.pack(side="right", fill="y")

tk.Label(right, text="Signup", font=("Arial", 22, "bold"), bg="#E6E6E6").pack(pady=20)

def create_entry(label, hide=False):
    tk.Label(right, text=label, bg="#E6E6E6").pack(anchor="w", padx=30)
    e = tk.Entry(right, show="*" if hide else "", width=30)
    e.pack(padx=30, pady=5)
    return e

entry_name = create_entry("Full Name")
entry_phone = create_entry("Phone")
entry_email = create_entry("Email")
entry_password = create_entry("Password", True)
entry_confirm = create_entry("Confirm Password", True)


# ---------- CONNECT FRONTEND TO BACKEND ----------
def handle_signup():
    result = signup_user(
        entry_name.get(),
        entry_phone.get(),
        entry_email.get(),
        entry_password.get(),
        entry_confirm.get()
    )

    if result == "SUCCESS":
        messagebox.showinfo("Success", "Signup completed")
    else:
        messagebox.showerror("Error", result)


tk.Button(
    right,
    text="Signup",
    command=handle_signup,
    bg="#6C7CFF",
    fg="white",
    width=20
).pack(pady=20)

>>>>>>> 9d431f1ab5dccf4c25302d4bd7c5adf2ac7dbf04
root.mainloop()