from .conn_db import ConnectDB
from tkinter import messagebox

def create_budget_table():
    conn_db = ConnectDB()

    sql = ('''CREATE TABLE budget (
                        id INTEGER,
                        name TEXT,
                        amount REAL,
                        PRIMARY KEY (id AUTOINCREMENT)
                    )''')
    
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Table budget created.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table budget already exists.'
        messagebox.showerror(title, message)

class Budget:
    def __init__(self, name, amount):
        self.id = None
        self.name = name
        self.amount = amount
        
def insert_budget(budget):
        conn_db = ConnectDB()

        sql = f"""INSERT INTO budget (name, amount) 
                VALUES ('{budget.name}', '{budget.amount}')"""
            
        try:
            conn_db.cursor.execute(sql)
            conn_db.close_connection()
            title = 'Connection'
            message = 'Data inserted into budget table.'
            messagebox.showinfo(title, message)
        except:
            title = 'Connection'
            message = 'Table budget does not exist.'
            messagebox.showerror(title, message)

def fetch_budgets():
    conn_db = ConnectDB()

    budget_fetched = []
    sql = "SELECT * FROM budget"

    try:
        conn_db.cursor.execute(sql)
        budget_fetched = conn_db.cursor.fetchall()
        conn_db.close_connection()
    except:
        title = 'Connection'
        message = 'Table budget does not exist.'
        messagebox.showerror(title, message)
    return budget_fetched

def edit_budget(budget, id):
    conn_db = ConnectDB()

    sql = f"""UPDATE budget 
              SET name = '{budget.name}', amount = '{budget.amount}' 
              WHERE id = {id}"""
    
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Data updated in budget table.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table budget does not exist.'
        messagebox.showerror(title, message)

def delete_budget(id):
    conn_db = ConnectDB()

    sql = f"""DELETE FROM budget 
              WHERE id = {id}"""
    
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Data deleted from budget table.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table budget does not exist.'
        messagebox.showerror(title, message)