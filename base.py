
import sqlite3

# -----------------
# Database setup
# -----------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

# -----------------
# Functions
# -----------------
def add_expense(date, category, amount, description):
    cursor.execute(
        "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
        (date, category, float(amount), description)
    )
    conn.commit()

def get_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")
    return cursor.fetchall()

def delete_expense(expense_id):
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

def filter_by_category(category):
    cursor.execute("SELECT * FROM expenses WHERE category LIKE ? ORDER BY date DESC, id DESC", (f"%{category}%",))
    return cursor.fetchall()

def get_total(category=None):
    if category:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category LIKE ?", (f"%{category}%",))
    else:
        cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    return total or 0.0

