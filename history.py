import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import database


class HistoryPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#F5F0F6")
        self.db = database.db
        self.controller = controller
        self.selected_transaction = None
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#F5F0F6")
        header.pack(fill=tk.X, padx=30, pady=20)
        tk.Label(header, text="📅 Transaction History", font=("Arial", 24, "bold"), bg="#F5F0F6", fg="#4A235A").pack(anchor="w")
        tk.Label(header, text="View and manage all your transactions", font=("Arial", 11), bg="#F5F0F6", fg="#666").pack(anchor="w")

        # Create a frame for the table
        table_frame = tk.Frame(self, bg="white", relief=tk.FLAT)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", font=("Arial", 11), rowheight=35, background="#F8F8F8", 
                       fieldbackground="#F8F8F8", borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4A235A", 
                       foreground="white", borderwidth=0)
        style.map('Treeview', background=[('selected', '#D5F5E3')], foreground=[('selected', '#000')])

        # Create Treeview with columns
        columns = ("ID", "Type", "Category", "Amount", "Date", "Actions")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Define headings and widths
        tree.heading("ID", text="ID")
        tree.heading("Type", text="Type")
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.heading("Actions", text="Actions")
        
        tree.column("ID", width=50, anchor="center")
        tree.column("Type", width=80, anchor="center")
        tree.column("Category", width=100, anchor="center")
        tree.column("Amount", width=100, anchor="e")
        tree.column("Date", width=100, anchor="center")
        tree.column("Actions", width=150, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.pack(fill=tk.BOTH, expand=True)

        # Store tree reference
        self.tree = tree

        # Fetch and populate data
        self.populate_table()

        # Bind row selection and click events
        tree.bind('<<TreeviewSelect>>', self.on_row_select)
        tree.bind('<Button-1>', self.on_tree_click)  # Detect direct cell clicks

        # Add summary frame at bottom
        summary_frame = tk.Frame(self, bg="#F5F0F6")
        summary_frame.pack(fill=tk.X, padx=30, pady=20)

        # Calculate totals and display summary
        self.update_summary(summary_frame)

    def populate_table(self):
        """Populate table with transaction data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch data from database
        rows = self.db.cursor.execute(
            "SELECT id, type, category, amount, date FROM tx ORDER BY date DESC"
        ).fetchall()

        for i, row in enumerate(rows):
            item_id = row[0]
            trans_type = row[1]
            category = row[2]
            amount = f"Rs. {row[3]:,.2f}"
            date = row[4]
            actions = "✏️ Edit  🗑️ Delete"
            
            # Insert row with tag for color coding
            tag = "income" if trans_type == "Income" else "expense"
            self.tree.insert("", "end", iid=item_id, values=(item_id, trans_type, category, amount, date, actions), tags=(tag,))

        # Configure row colors based on type
        self.tree.tag_configure("income", background="#D5F5E3", foreground="#27AE60")
        self.tree.tag_configure("expense", background="#FADBD8", foreground="#C0392B")

    def on_row_select(self, event):
        """Handle row selection"""
        selection = self.tree.selection()
        if selection:
            self.selected_transaction = selection[0]

    def on_tree_click(self, event):
        """Handle direct clicks on the tree (including Actions column)"""
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        
        if not row:
            return
        
        # Set the selected transaction
        self.selected_transaction = row
        
        # Check if Actions column was clicked (column #6)
        if column == "#6":
            # Get the cell bounding box to determine if Edit or Delete was clicked
            try:
                bbox = self.tree.bbox(row, column)
                if bbox:
                    # Split cell in half: left = Edit, right = Delete
                    cell_left = bbox[0]
                    cell_width = bbox[2]
                    cell_midpoint = cell_left + (cell_width / 2)
                    
                    if event.x < cell_midpoint:
                        # Clicked on left side (Edit)
                        self.edit_transaction()
                    else:
                        # Clicked on right side (Delete)
                        self.delete_transaction()
            except:
                pass


    def update_summary(self, parent):
        """Update summary cards with totals"""
        # Clear existing widgets
        for w in parent.winfo_children():
            w.destroy()

        # Calculate totals
        all_rows = self.db.cursor.execute(
            "SELECT type, amount FROM tx"
        ).fetchall()
        
        total_income = sum(row[1] for row in all_rows if row[0] == "Income")
        total_expense = sum(row[1] for row in all_rows if row[0] == "Expense")
        net = total_income - total_expense

        # Summary cards
        card_frame = tk.Frame(parent, bg="white", relief=tk.FLAT)
        card_frame.pack(fill=tk.X)

        # Income Card
        income_card = tk.Frame(card_frame, bg="#D5F5E3", relief=tk.FLAT)
        income_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(income_card, text="Total Income", font=("Arial", 10), bg="#D5F5E3", fg="#27AE60").pack(pady=(10, 5))
        tk.Label(income_card, text=f"Rs. {total_income:,.2f}", font=("Arial", 14, "bold"), bg="#D5F5E3", fg="#27AE60").pack(pady=(5, 10))

        # Expense Card
        expense_card = tk.Frame(card_frame, bg="#FADBD8", relief=tk.FLAT)
        expense_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(expense_card, text="Total Expenses", font=("Arial", 10), bg="#FADBD8", fg="#C0392B").pack(pady=(10, 5))
        tk.Label(expense_card, text=f"Rs. {total_expense:,.2f}", font=("Arial", 14, "bold"), bg="#FADBD8", fg="#C0392B").pack(pady=(5, 10))

        # Net Card
        net_card = tk.Frame(card_frame, bg="#F3E5F5", relief=tk.FLAT)
        net_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(net_card, text="Net Balance", font=("Arial", 10), bg="#F3E5F5", fg="#8E44AD").pack(pady=(10, 5))
        tk.Label(net_card, text=f"Rs. {net:,.2f}", font=("Arial", 14, "bold"), bg="#F3E5F5", fg="#8E44AD").pack(pady=(5, 10))

        # Action buttons frame
        action_frame = tk.Frame(parent, bg="#F5F0F6")
        action_frame.pack(fill=tk.X, pady=(15, 0))

        tk.Button(action_frame, text="✏️ Edit Selected", command=self.edit_transaction,
                 bg="#3498DB", fg="white", font=("Arial", 11, "bold"),
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=20, pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(action_frame, text="🗑️ Delete Selected", command=self.delete_transaction,
                 bg="#E74C3C", fg="white", font=("Arial", 11, "bold"),
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=20, pady=8).pack(side=tk.LEFT, padx=5)

    def edit_transaction(self):
        """Edit selected transaction"""
        if not self.selected_transaction:
            messagebox.showwarning("Warning", "Please select a transaction to edit")
            return

        # Fetch current transaction data
        row = self.db.cursor.execute(
            "SELECT type, category, amount, date FROM tx WHERE id = ?",
            (int(self.selected_transaction),)
        ).fetchone()

        if not row:
            messagebox.showerror("Error", "Transaction not found")
            return

        trans_type, category, amount, date = row

        # Create edit dialog
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Transaction")
        edit_window.geometry("400x300")
        edit_window.configure(bg="white")

        # Title
        tk.Label(edit_window, text="Edit Transaction", font=("Arial", 16, "bold"), bg="white", fg="#4A235A").pack(pady=15)

        # Form frame
        form = tk.Frame(edit_window, bg="white")
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Type (read-only)
        tk.Label(form, text="Type:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(form, text=trans_type, font=("Arial", 11), bg="#F0F0F0").pack(fill=tk.X, pady=(0, 15))

        # Category (read-only)
        tk.Label(form, text="Category:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(form, text=category, font=("Arial", 11), bg="#F0F0F0").pack(fill=tk.X, pady=(0, 15))

        # Amount
        tk.Label(form, text="Amount:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        amount_entry = tk.Entry(form, font=("Arial", 11), relief=tk.FLAT, bg="#F8F8F8", bd=0)
        amount_entry.insert(0, str(amount))
        amount_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Date
        tk.Label(form, text="Date (YYYY/MM/DD):", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        date_entry = tk.Entry(form, font=("Arial", 11), relief=tk.FLAT, bg="#F8F8F8", bd=0)
        date_entry.insert(0, date)
        date_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Buttons
        btn_frame = tk.Frame(form, bg="white")
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        def save_changes():
            try:
                new_amount = float(amount_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return

            new_date = date_entry.get().strip()

            try:
                datetime.strptime(new_date, "%Y/%m/%d")
            except ValueError:
                messagebox.showerror("Error", "Date format must be YYYY/MM/DD")
                return

            # Update database
            try:
                self.db.cursor.execute(
                    "UPDATE tx SET amount = ?, date = ? WHERE id = ?",
                    (new_amount, new_date, int(self.selected_transaction))
                )
                self.db.conn.commit()
                messagebox.showinfo("Success", "✓ Transaction updated successfully")
                edit_window.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")

        tk.Button(btn_frame, text="💾 Save Changes", command=save_changes,
                 bg="#27AE60", fg="white", font=("Arial", 11, "bold"),
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=15, pady=8).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="❌ Cancel", command=edit_window.destroy,
                 bg="#95A5A6", fg="white", font=("Arial", 11, "bold"),
                 relief=tk.FLAT, bd=0, cursor="hand2", padx=15, pady=8).pack(side=tk.LEFT, padx=5)

    def delete_transaction(self):
        """Delete selected transaction"""
        if not self.selected_transaction:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return

        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
        if not result:
            return

        try:
            self.db.cursor.execute("DELETE FROM tx WHERE id = ?", (int(self.selected_transaction),))
            self.db.conn.commit()
            messagebox.showinfo("Success", "✓ Transaction deleted successfully")
            self.selected_transaction = None
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {str(e)}")

    def refresh(self):
        """Refresh the page when shown"""
        # Clear and rebuild table
        for w in self.winfo_children():
            w.destroy()
        self.setup_ui()
        
        # Refresh Report tab if it exists
        if self.controller and "Report" in self.controller.frames:
            if hasattr(self.controller.frames["Report"], "refresh"):
                # Don't call directly, just mark for refresh when shown
                pass
