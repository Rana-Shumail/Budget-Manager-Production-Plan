import requests
from tkinter import messagebox
import json

API_URL = 'https://budget-manager-production-plan.onrender.com/'

#def create_goal_table():
    # conn_db = ConnectDB()

    # sql = ('''CREATE TABLE goal (
    #                    id_goal INTEGER,
    #                    name_goal TEXT,
    #                    amount_goal REAL,
    #                    PRIMARY KEY (id_goal AUTOINCREMENT)
    #                )''')
    #try:
    #    conn_db.cursor.execute(sql)
    #    conn_db.close_connection()
    #    title = 'Connection'
    #    message = 'Table Goal created.'
    #    messagebox.showinfo(title, message)
    #except:
    #    title = 'Connection'
    #    message = 'Table Goal already exists.'
    #    messagebox.showerror(title, message)

class Goal:
    def __init__(self, name_goal, amount_goal):
        self.id_goal = None
        self.name_goal = name_goal
        self.amount_goal = amount_goal

def insert_goal(goal):
        #conn_db = ConnectDB()

        #sql = """INSERT INTO goal (name_goal, amount_goal) 
        #        VALUES (?, ?)"""

        """Inserts a new goal via a POST request to the API"""
        endpoint = f"{API_URL}goals"

        # Payload
        payload = {
        "name_goal": goal.name_goal,
        "amount_goal": goal.amount_goal
        }

        try:
        #    conn_db.cursor.execute(sql, (goal.name_goal, goal.amount_goal))
        #    conn_db.close_connection()

            response = requests.post(endpoint, json = payload)
            response.raise_for_status() # Raise error for 4xx/5xx status codes

            title = 'Connection'
            message = 'Data inserted into Goal table via API.'
            messagebox.showinfo(title, message)
            return True # Success
        except requests.exceptions.RequestException as e:
            title = 'Connection'
            message = f'Could not insert data into Goal table via API: {e}'
            messagebox.showerror(title, message)
            return False # Failure

def fetch_goals():
    #conn_db = ConnectDB()

    """Fetches all goals via a GET request and adapts the JSON format."""
    endpoint = f"{API_URL}goals"
    goal_fetched = []

    #sql = "SELECT * FROM goal"
    
    try:
        #conn_db.cursor.execute(sql)
        #goal_fetched = conn_db.cursor.fetchall()
        #conn_db.close_connection()

        response = requests.get(endpoint)
        response.raise_for_status()

        goals_json = response.json()

        # Convert JSON back to list of tuples to match SQLite format
        for g in goals_json:
            goal_tuple = (g.get('id_goal'), g.get('name_goal'), g.get('amount_goal'))
            goal_fetched.append(goal_tuple)
    except requests.exceptions.RequestException as e:
        title = 'Connection'
        message = f'Could not fetch goals from API: {e}'
        messagebox.showerror(title, message)

    return goal_fetched

def edit_goal(goal, id_goal):
    #conn_db = ConnectDB()

    #sql = """UPDATE goal 
    #          SET name_goal = ?, amount_goal = ? 
    #          WHERE id_goal = ?"""
    
    """Updates an existing goal via a PUT or PATCH request to the API."""
    endpoint = f"{API_URL}goals/{id_goal}"
    
    #Payload
    payload = {
        "name_goal": goal.name_goal,
        "amount_goal": goal.amount_goal
    }

    try:
        #conn_db.cursor.execute(sql, (goal.name_goal, goal.amount_goal, id_goal))
        #conn_db.close_connection()

        response = requests.put(endpoint, json = payload)
        response.raise_for_status()

        title = 'Connection'
        message = 'Data updated in Goal table via API.'
        messagebox.showinfo(title, message)
        return True
    except requests.exceptions.RequestException as e:
        title = 'Connection'
        message = f'Could not update data in Goal table via API: {e}'
        messagebox.showerror(title, message)
        return False

def delete_goal(id_goal):
    #conn_db = ConnectDB()

    #sql = """DELETE FROM goal 
    #          WHERE id_goal = ?"""
    
    """Deletes a goal via a DELETE request to the API."""
    endpoint = f"{API_URL}goals/{id_goal}"

    try:
        #conn_db.cursor.execute(sql, (id_goal,)) # Because id_goal is a single value, we need to pass it as a one-element tuple
        #conn_db.close_connection()

        response = requests.delete(endpoint)
        response.raise_for_status()

        title = 'Connection'
        message = 'Data deleted from Goal table via API.'
        messagebox.showinfo(title, message)
        return True
    except requests.exceptions.RequestException as e:
        title = 'Connection'
        message = f'Could not delete data from Goal table via API: {e}'
        messagebox.showerror(title, message)
        return False
