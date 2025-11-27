from .conn_db import ConnectDB
from tkinter import messagebox

def create_user_table():
    conn_db = ConnectDB()

    sql = ('''CREATE TABLE user (
                        email TEXT,
                        username TEXT,
                        password TEXT
                    )''')
    
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Table User created.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table User already exists.'
        messagebox.showerror(title, message)

class User:
    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password
        
def insert_user(user):
        conn_db = ConnectDB()

        sql = f"""INSERT INTO user (email, username, password) 
                VALUES ('{user.email}', '{user.username}', '{user.password}')"""
            
        try:
            conn_db.cursor.execute(sql)
            conn_db.close_connection()
            title = 'Connection'
            message = 'Data inserted into User table.'
            messagebox.showinfo(title, message)
        except:
            title = 'Connection'
            message = 'Table User does not exist.'
            messagebox.showerror(title, message)

def fetch_user():
    conn_db = ConnectDB()

    user_fetched = []
    sql = "SELECT * FROM user"

    try:
        conn_db.cursor.execute(sql)
        user_fetched = conn_db.cursor.fetchall()
        conn_db.close_connection()
    except:
        title = 'Connection'
        message = 'Table User does not exist.'
        messagebox.showerror(title, message)
    return user_fetched

def edit_user(user, email):
    conn_db = ConnectDB()

    sql = f"""UPDATE user 
              SET name = '{user.username}', amount = '{user.password}' 
              WHERE email = '{email}'"""
    
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Data updated in User table.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table User does not exist.'
        messagebox.showerror(title, message)

def delete_budget(email):
    conn_db = ConnectDB()

    sql = f"""DELETE FROM user 
              WHERE email = '{email}'"""
    
    try:
        conn_db.cursor.execute(sql)
        conn_db.close_connection()
        title = 'Connection'
        message = 'Data deleted from User table.'
        messagebox.showinfo(title, message)
    except:
        title = 'Connection'
        message = 'Table User does not exist.'
        messagebox.showerror(title, message)