from .conn_db import ConnectDB
from tkinter import messagebox

def create_goal_table():
    conn_db = ConnectDB()

    sql = ('''CREATE TABLE goal (
                        id_goal INTEGER,
                        name_goal TEXT,
                        amount_goal REAL,
                        PRIMARY KEY (id_goal AUTOINCREMENT)
                    )''')
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Table Goal created.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table Goal already exists.'
        messagebox.showerror(title, message)

class Goal:
    def __init__(self, name_goal, amount_goal):
        self.id_goal = None
        self.name_goal = name_goal
        self.amount_goal = amount_goal

def insert_goal(goal):
        conn_db = ConnectDB()

        sql = """INSERT INTO goal (name_goal, amount_goal) 
                VALUES (?, ?)"""
            
        try:
            conn_db.cursor.execute(sql, (goal.name_goal, goal.amount_goal))
            conn_db.close_connection()
            title = 'Connection'
            message = 'Data inserted into Goal table.'
            messagebox.showinfo(title, message)
        except:
            title = 'Connection'
            message = 'Could not insert data into Goal table.'
            messagebox.showerror(title, message)

def fetch_goals():
    conn_db = ConnectDB()

    goal_fetched = []
    sql = "SELECT * FROM goal"

    try:
        conn_db.cursor.execute(sql)
        goal_fetched = conn_db.cursor.fetchall()
        conn_db.close_connection()
    except:
        title = 'Connection'
        message = 'Table goal does not exist.'
        messagebox.showerror(title, message)

    return goal_fetched

def edit_goal(goal, id_goal):
    conn_db = ConnectDB()

    sql = """UPDATE goal 
              SET name_goal = ?, amount_goal = ? 
              WHERE id_goal = ?"""
    
    try:
        conn_db.cursor.execute(sql, (goal.name_goal, goal.amount_goal, id_goal))
        conn_db.close_connection()
        title = 'Connection'
        message = 'Data updated in Goal table.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Could not update data in Goal table.'
        messagebox.showerror(title, message)

def delete_goal(id_goal):
    conn_db = ConnectDB()

    sql = """DELETE FROM goal 
              WHERE id_goal = ?"""
    
    try:
        conn_db.cursor.execute(sql, (id_goal,)) # Because id_goal is a single value, we need to pass it as a one-element tuple
        conn_db.close_connection()
        title = 'Connection'
        message = 'Data deleted from Goal table.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table Goal does not exist.'
        messagebox.showerror(title, message)