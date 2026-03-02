import tkinter as tk
from tkinter import messagebox, font
import home, income, expenses, report, settings
import history
import database
import sqlite3
import re
import os


# --- Authentication Functions ---
def init_db():
    """Initialize the users database"""
    # Ensure signup directory exists
    os.makedirs("signup", exist_ok=True)
    conn = sqlite3.connect("signup/users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        phone TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()


def login_user(email, password):
    """Authenticate user"""
    if not all([email, password]):
        return "All fields are required"

    try:
        conn = sqlite3.connect("signup/users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return "SUCCESS"
        else:
            return "Invalid email or password"
    except Exception as e:
        return str(e) or "An error occurred"


def signup_user(fullname, phone, email, password, confirm):
    """Register a new user"""
    if not all([fullname, phone, email, password, confirm]):
        return "All fields are required"

    if password != confirm:
        return "Passwords do not match"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format"

    try:
        conn = sqlite3.connect("signup/users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (fullname, phone, email, password) VALUES (?, ?, ?, ?)",
            (fullname, phone, email, password)
        )
        conn.commit()
        conn.close()
        return "SUCCESS"
    except sqlite3.IntegrityError:
        return "Email already exists"
    except Exception as e:
        return str(e) or "An error occurred"


# --- Authentication Window ---
class AuthWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Management System")
        self.geometry("900x500")
        self.resizable(False, False)
        self.authenticated_user = None
        self.login_image = None
        self.signup_image = None
        
        # Initialize database
        init_db()
        
        self.show_login()

    def show_login(self):
        """Display login form with image"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()

        # Left Frame - Image
        left_frame = tk.Frame(self, width=550, height=500, bg="white")
        left_frame.pack(side="left", fill="both")

        # Load image
        img_path = os.path.join(os.path.dirname(__file__), "signup", "login.png")
        try:
            from PIL import Image, ImageTk
            img = Image.open(img_path)
            img = img.resize((450, 350), Image.LANCZOS)
            self.login_image = ImageTk.PhotoImage(img)
            img_label = tk.Label(left_frame, image=self.login_image, bg="white")
            img_label.pack(expand=True)
        except Exception:
            tk.Label(left_frame, text="No image available", bg="white", fg="#666").pack(expand=True)

        # Right Frame - Form
        right_frame = tk.Frame(self, bg="#E6E6E6", width=350)
        right_frame.pack(side="right", fill="y")

        tk.Label(right_frame, text="login", font=("Arial", 22, "bold"), bg="#E6E6E6").pack(pady=20)

        tk.Label(right_frame, text="Email", bg="#E6E6E6").pack(anchor="w", padx=30)
        email_entry = tk.Entry(right_frame, font=("Arial", 12), width=30)
        email_entry.pack(padx=30, pady=5)

        tk.Label(right_frame, text="Password", bg="#E6E6E6").pack(anchor="w", padx=30)
        password_entry = tk.Entry(right_frame, show="*", font=("Arial", 12), width=30)
        password_entry.pack(padx=30, pady=5)

        def handle_login():
            result = login_user(email_entry.get(), password_entry.get())
            if result == "SUCCESS":
                self.authenticated_user = email_entry.get()
                self.destroy()
            else:
                messagebox.showerror("Login Failed", result)

        tk.Button(
            right_frame,
            text="login",
            command=handle_login,
            bg="#6C7CFF",
            fg="white",
            width=20
        ).pack(pady=20)

        tk.Label(right_frame, text="Don't have an account?", bg="#E6E6E6").pack(pady=10)
        tk.Button(
            right_frame,
            text="Signup",
            command=self.show_signup,
            bg="#6C7CFF",
            fg="white",
            width=20
        ).pack(pady=10)

    def show_signup(self):
        """Display signup form with image"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()

        # Left Frame - Image
        left_frame = tk.Frame(self, width=550, height=500, bg="white")
        left_frame.pack(side="left", fill="both")

        # Load image
        img_path = os.path.join(os.path.dirname(__file__), "signup", "Image.png")
        try:
            from PIL import Image, ImageTk
            img = Image.open(img_path)
            img = img.resize((450, 350), Image.LANCZOS)
            self.signup_image = ImageTk.PhotoImage(img)
            img_label = tk.Label(left_frame, image=self.signup_image, bg="white")
            img_label.pack(expand=True)
        except Exception:
            tk.Label(left_frame, text="No image available", bg="white", fg="#666").pack(expand=True)

        # Right Frame - Form
        right_frame = tk.Frame(self, bg="#E6E6E6", width=350)
        right_frame.pack(side="right", fill="y")

        tk.Label(right_frame, text="Signup", font=("Arial", 22, "bold"), bg="#E6E6E6").pack(pady=20)

        tk.Label(right_frame, text="fullname", bg="#E6E6E6").pack(anchor="w", padx=30)
        name_entry = tk.Entry(right_frame, font=("Arial", 12), width=30)
        name_entry.pack(padx=30, pady=5)

        tk.Label(right_frame, text="Phone", bg="#E6E6E6").pack(anchor="w", padx=30)
        phone_entry = tk.Entry(right_frame, font=("Arial", 12), width=30)
        phone_entry.pack(padx=30, pady=5)

        tk.Label(right_frame, text="Email", bg="#E6E6E6").pack(anchor="w", padx=30)
        email_entry = tk.Entry(right_frame, font=("Arial", 12), width=30)
        email_entry.pack(padx=30, pady=5)

        tk.Label(right_frame, text="Password", bg="#E6E6E6").pack(anchor="w", padx=30)
        password_entry = tk.Entry(right_frame, show="*", font=("Arial", 12), width=30)
        password_entry.pack(padx=30, pady=5)

        tk.Label(right_frame, text="Confirm Password", bg="#E6E6E6").pack(anchor="w", padx=30)
        confirm_entry = tk.Entry(right_frame, show="*", font=("Arial", 12), width=30)
        confirm_entry.pack(padx=30, pady=5)

        def handle_signup():
            result = signup_user(
                name_entry.get(),
                phone_entry.get(),
                email_entry.get(),
                password_entry.get(),
                confirm_entry.get()
            )
            if result == "SUCCESS":
                messagebox.showinfo("Success", "Signup completed")
                self.show_login()
            else:
                messagebox.showerror("Error", result)

        tk.Button(
            right_frame,
            text="Signup",
            command=handle_signup,
            bg="#6C7CFF",
            fg="white",
            width=20
        ).pack(pady=20)


class BudgetApp(tk.Tk):
    def __init__(self, authenticated_user_email=None):
        super().__init__()
        self.title("Budget Management System")
        self.geometry("1100x750")
        self.authenticated_user_email = authenticated_user_email

        # colour palette copied from riwaj.py for consistency
        self.colors = {
            "sidebar": "#FDB913",
            "active_tab": "#FAD7A0",
            "bg": "#F5F0F6",
            "header": "#4A235A",
            "green_card": "#D5F5E3",
            "pink_card": "#FADBD8",
            # category colours may be used by pages
            "rent": "#5D6D7E", "food": "#F4D03F", "savings": "#C0392B",
            "groceries": "#8E44AD", "study": "#EB70AA", "bike": "#2ECC71"
        }

        self.configure(bg=self.colors["bg"])

        # Navigation State
        self.frames = {}
        self.pages = {
            "Home": home.HomePage,
            "Report": report.ReportPage,
            "Add income": income.IncomePage,
            "Add Expenses": expenses.ExpensesPage,
            "Update": settings.SettingsPage,
            "History": history.HistoryPage
        }

        # UI Layout
        self.header = tk.Frame(self, bg=self.colors["header"], height=70)
        self.header.pack(side=tk.TOP, fill=tk.X)
        self.header.pack_propagate(False)
        tk.Label(self.header, text="🔔", font=("Arial", 18), bg=self.colors["header"]).pack(side="left", padx=20)
        tk.Label(self.header, text="Budget Management System", fg="white", 
                 bg=self.colors["header"], font=("Arial", 20, "bold")).pack(pady=15)
        tk.Label(self.header, text="👤\nAccount", fg="white", bg=self.colors["header"],
                 font=("Arial", 9)).pack(side="right", padx=20)

        self.sidebar = tk.Frame(self, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self, bg=self.colors["bg"])
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_nav()
        self.create_pages()
        self.show_page("Home")

    def setup_nav(self):
        # each tuple is (label shown on button, page key or special action)
        menu_items = [
            ("🏠 Home", "Home"),
            ("📊 Report", "Report"),
            ("➕ Add income", "Add income"),
            ("➕ Add Expenses", "Add Expenses"),
            ("📅 History", "History"),
            ("✏️ Update", "Update"),
            ("🔒 Logout", "Logout"),
        ]

        self.nav_buttons = {}
        for label, key in menu_items:
            if key == "Logout":
                cmd = self.logout
            else:
                cmd = lambda k=key: self.show_page(k)

            btn = tk.Button(self.sidebar, text=label, bg=self.colors["sidebar"], fg="black",
                            font=("Arial", 12), relief=tk.FLAT, pady=15, anchor="w", padx=20,
                            command=cmd, cursor="hand2")
            btn.pack(fill=tk.X, pady=1)
            self.nav_buttons[key] = btn

    def create_pages(self):
        """Create all page frames upfront and stack them using grid"""
        for page_name, page_class in self.pages.items():
            frame = page_class(self.content, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    def show_page(self, name):
        """Raise the specified frame and refresh it"""
        # special case for logout
        if name == "Logout":
            return self.logout()

        if name not in self.frames:
            return

        # update nav button highlights
        for key, btn in self.nav_buttons.items():
            btn.configure(bg=self.colors["sidebar"])
        if name in self.nav_buttons:
            self.nav_buttons[name].configure(bg=self.colors["active_tab"])

        # Raise the frame to the top
        frame = self.frames[name]
        frame.tkraise()
        
        # Refresh the page if it has a refresh method
        if hasattr(frame, "refresh"):
            frame.refresh()

    def logout(self):
        """Logout and return to authentication"""
        try:
            self.destroy()
        except Exception:
            pass
        try:
            # Restart the authentication flow
            auth_window = AuthWindow()
            auth_window.mainloop()
            if auth_window.authenticated_user:
                # Initialize user config in database
                database.db.init_user_config(auth_window.authenticated_user)
                app = BudgetApp(authenticated_user_email=auth_window.authenticated_user)
                app.mainloop()
        except Exception:
            pass

if __name__ == "__main__":
    # First show authentication window
    auth_window = AuthWindow()
    auth_window.mainloop()
    
    # Only proceed if user authenticated successfully
    if auth_window.authenticated_user:
        # Initialize user config in database
        database.db.init_user_config(auth_window.authenticated_user)
        app = BudgetApp(authenticated_user_email=auth_window.authenticated_user)
        app.mainloop()
