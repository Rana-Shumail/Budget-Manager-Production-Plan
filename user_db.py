import psycopg2
import os

# Your Render URL
DB_URL = os.environ.get('DATABASE_URL', "postgresql://usersbudbuddy_user:lM6hObuSlCwaegoFiwhxn0Wv0XGNDAog@dpg-d4lp420gjchc73arqh8g-a.oregon-postgres.render.com/usersbudbuddy")

def connect():
    return psycopg2.connect(DB_URL, sslmode='require')

def create_table():
    conn = connect()
    cur = conn.cursor()
    
    # 1. Users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    
    # 2. Goals
    cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            target NUMERIC,
            current NUMERIC,
            deadline TEXT,
            FOREIGN KEY (username) REFERENCES users (username)
        );
    """)

    # 3. Budgets
    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            category TEXT,
            amount NUMERIC
        );
    """)

    # 4. NEW: Expenses (Linked to a Budget ID)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            budget_id INTEGER REFERENCES budgets(id) ON DELETE CASCADE,
            description TEXT,
            amount NUMERIC,
            date TEXT
        );
    """)
    
    conn.commit()
    conn.close()

# --- HELPER FUNCTIONS ---

def get_budgets_with_spending(username):
    """Fetches budgets AND calculates the total spent/remaining for each."""
    conn = connect()
    cur = conn.cursor()
    # SQL query that sums up expenses for each budget automatically
    query = """
        SELECT b.id, b.category, b.amount, COALESCE(SUM(e.amount), 0) as spent
        FROM budgets b
        LEFT JOIN expenses e ON b.id = e.budget_id
        WHERE b.username = %s
        GROUP BY b.id
        ORDER BY b.id DESC
    """
    cur.execute(query, (username,))
    rows = cur.fetchall()
    conn.close()
    
    budgets = []
    for row in rows:
        budgets.append({
            "id": row[0],
            "category": row[1],
            "limit": float(row[2]),
            "spent": float(row[3]),
            "remaining": float(row[2]) - float(row[3])
        })
    return budgets

def add_expense(budget_id, description, amount, date):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (budget_id, description, amount, date) VALUES (%s, %s, %s, %s)",
        (budget_id, description, amount, date)
    )
    conn.commit()
    conn.close()

# --- BASIC CRUD ---
def add_budget(username, category, amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO budgets (username, category, amount) VALUES (%s, %s, %s)", (username, category, amount))
    conn.commit()
    conn.close()

def delete_budget(budget_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM budgets WHERE id = %s", (budget_id,))
    conn.commit()
    conn.close()

# --- USER/GOAL FUNCTIONS ---
def insert_user(username, password):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except Exception as e:
        conn.rollback(); raise e
    finally:
        conn.close()

def validate_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    res = cur.fetchone()
    conn.close()
    return res is not None

def update_password(username, email, new_password):
    conn = connect()
    cur = conn.cursor()
    
    # Run the Update command directly checking both Username AND Email
    cur.execute("""
        UPDATE users 
        SET password = %s 
        WHERE username = %s AND email = %s
    """, (new_password, username, email))
    
    # Check if any row was actually changed
    rows_affected = cur.rowcount
    
    conn.commit()
    conn.close()
    
    # Returns True if found & updated, False if no match found
    return rows_affected > 0
    
    # Update password
    cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    conn.commit()
    conn.close()
    return True

def add_goal(username, title, target, current, date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO goals (username, title, target, current, deadline) VALUES (%s, %s, %s, %s, %s)", (username, title, target, current, date))
    conn.commit()
    conn.close()

def get_goals(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, title, target, current, deadline FROM goals WHERE username = %s", (username,))
    rows = cur.fetchall()
    conn.close()
    return [{"id":r[0], "title":r[1], "target":float(r[2]), "current":float(r[3]), "date":r[4]} for r in rows]

def update_goal(gid, t, tgt, cur_amt, d):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE goals SET title=%s, target=%s, current=%s, deadline=%s WHERE id=%s", (t, tgt, cur_amt, d, gid))
    conn.commit()
    conn.close()

def get_dashboard_stats(username):
    conn = connect()
    cur = conn.cursor()
    
    # 1. Total Planned Budget 
    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM budgets WHERE username = %s", (username,))
    total_budget = float(cur.fetchone()[0])

    # 2. Total Expenses 
    cur.execute("""
        SELECT COALESCE(SUM(e.amount), 0) 
        FROM expenses e 
        JOIN budgets b ON e.budget_id = b.id 
        WHERE b.username = %s
    """, (username,))
    total_expenses = float(cur.fetchone()[0])

    conn.close()
    
    # 3. Calculate "Remaining Balance"
    remaining_balance = total_budget - total_expenses

    return {
        "remaining_balance": remaining_balance, # Used for "Total Balance" card
        "total_budget": total_budget,           # Used for "Monthly Budget" card
        "total_expenses": total_expenses        # Used for "Total Expenses" card
    }

# --- EXECUTION BLOCK  ---
if __name__ == "__main__":
    try:
        create_table()
        print("Tables (Users, Goals, Budgets, Expenses) initialized!")
    except Exception as e:
        print(f"Error: {e}")
