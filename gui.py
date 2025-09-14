# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import base   # <-- import backend functions

def load_expenses(data=None):
    for row in tree.get_children():
        tree.delete(row)
    rows = data if data else base.get_expenses()
    for row in rows:
        tree.insert("", tk.END, values=row)
    total_label.config(text=f"Total: ₹{base.get_total():.2f}")

def add_expense():
    date = date_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()
    description = description_entry.get().strip()
    if not date or not category or not amount:
        messagebox.showwarning("Input Error", "Date, Category, and Amount are required!")
        return
    try:
        base.add_expense(date, category, float(amount), description)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be numeric.")
        return
    clear_entries()
    load_expenses()

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Delete Error", "Select an expense to delete.")
        return
    expense_id = tree.item(selected[0])['values'][0]
    if messagebox.askyesno("Confirm", "Delete this expense?"):
        base.delete_expense(expense_id)
        load_expenses()

def filter_expenses():
    category = category_entry.get().strip()
    if not category:
        load_expenses()
        return
    rows = base.filter_by_category(category)
    load_expenses(rows)
    total_label.config(text=f"Filtered Total: ₹{base.get_total(category):.2f}")

def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# -----------------------
# GUI Layout
# -----------------------
root = tk.Tk()
root.title("Expense Tracker (GUI)")

# Inputs
tk.Label(root, text="Date").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Category").grid(row=0, column=2, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text="Amount").grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Description").grid(row=1, column=2, padx=5, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=3, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Delete Selected", command=delete_selected).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Filter by Category", command=filter_expenses).grid(row=2, column=2, padx=5, pady=5)
tk.Button(root, text="Show All", command=load_expenses).grid(row=2, column=3, padx=5, pady=5)

# Treeview
columns = ("ID", "Date", "Category", "Amount", "Description")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Total Label
total_label = tk.Label(root, text="Total: ₹0.00", font=("Arial", 12, "bold"))
total_label.grid(row=4, column=0, columnspan=4, pady=5)

# Make grid expand
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Load data initially
load_expenses()

root.mainloop()
