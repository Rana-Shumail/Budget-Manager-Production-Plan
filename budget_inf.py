import requests
from tkinter import messagebox
import json

API_URL = 'https://budget-manager-production-plan.onrender.com/'

#def create_budget_table():
    #conn_db = ConnectDB()

    #sql = ('''CREATE TABLE budget (
    #                    id INTEGER,
    #                    name TEXT,
    #                    amount REAL,
    #                    PRIMARY KEY (id AUTOINCREMENT)
    #                )''')
    
    #try:
    #    conn_db.cursor.execute(sql)
    #    conn_db.close_connection()
    #    title = 'Connection'
    #    message = 'Table budget created.'
    #    messagebox.showinfo(title, message)
    #except:
    #    title = 'Connection'
    #    message = 'Table budget already exists.'
    #    messagebox.showerror(title, message)

class Budget:
    def __init__(self, name, amount):
        self.id = None
        self.name = name
        self.amount = amount
        
def insert_budget(budget):
        #conn_db = ConnectDB()

        #sql = f"""INSERT INTO budget (name, amount) 
        #        VALUES ('{budget.name}', '{budget.amount}')"""

        """Inserts a new budget via a POST request to the API"""
        endpoint = f"{API_URL}budgets"

        # Payload
        payload = {
        "name": budget.name,
        "amount": budget.amount
        }

        try:
        #    conn_db.cursor.execute(sql, (goal.name_goal, goal.amount_goal))
        #    conn_db.close_connection()

            response = requests.post(endpoint, json = payload)
            response.raise_for_status() # Raise error for 4xx/5xx status codes

            title = 'Connection'
            message = 'Data inserted into Budget table via API.'
            messagebox.showinfo(title, message)
            return True # Success
        except requests.exceptions.RequestException as e:
            title = 'Connection'
            message = f'Could not insert data into Budget table via API: {e}'
            messagebox.showerror(title, message)
            return False # Failure

def fetch_budgets():
    #conn_db = ConnectDB()

    #sql = "SELECT * FROM budget"

    """Fetches all budgets via a GET request and adapts the JSON format."""
    endpoint = f"{API_URL}budgets"
    budget_fetched = []

    #sql = "SELECT * FROM budget"
    
    try:
        #conn_db.cursor.execute(sql)
        #goal_fetched = conn_db.cursor.fetchall()
        #conn_db.close_connection()

        response = requests.get(endpoint)
        response.raise_for_status()

        budgets_json = response.json()

        # Convert JSON back to list of tuples to match SQLite format
        for b in budgets_json:
            goal_tuple = (b.get('id'), b.get('name'), b.get('amount'))
            budget_fetched.append(goal_tuple)
    except requests.exceptions.RequestException as e:
        title = 'Connection'
        message = f'Could not fetch budgets from API: {e}'
        messagebox.showerror(title, message)

    return budget_fetched

def edit_budget(budget, id):
    #conn_db = ConnectDB()

    #sql = f"""UPDATE budget 
    #          SET name = '{budget.name}', amount = '{budget.amount}' 
    #          WHERE id = {id}"""
    
    """Updates an existing budget via a PUT or PATCH request to the API."""
    endpoint = f"{API_URL}budgets/{id}"
    
    #Payload
    payload = {
        "name": budget.name,
        "amount": budget.amount
    }

    try:
        #conn_db.cursor.execute(sql, (goal.name_goal, goal.amount_goal, id_goal))
        #conn_db.close_connection()

        response = requests.put(endpoint, json = payload)
        response.raise_for_status()

        title = 'Connection'
        message = 'Data updated in Budget table via API.'
        messagebox.showinfo(title, message)
        return True
    except requests.exceptions.RequestException as e:
        title = 'Connection'
        message = f'Could not update data in Budget table via API: {e}'
        messagebox.showerror(title, message)
        return False

def delete_budget(id):
    #conn_db = ConnectDB()

    #sql = f"""DELETE FROM budget 
    #          WHERE id = {id}"""
    
    """Deletes a budget via a DELETE request to the API."""
    endpoint = f"{API_URL}budgets/{id}"

    try:
        #conn_db.cursor.execute(sql, (id_goal,)) # Because id_goal is a single value, we need to pass it as a one-element tuple
        #conn_db.close_connection()

        response = requests.delete(endpoint)
        response.raise_for_status()

        title = 'Connection'
        message = 'Data deleted from Budget table via API.'
        messagebox.showinfo(title, message)
        return True
    except requests.exceptions.RequestException as e:
        title = 'Connection'
        message = f'Could not delete data from Budget table via API: {e}'
        messagebox.showerror(title, message)
        return False
