import sqlite3
import budgets_db
import user_db
import goals_db

# Display budgets in database
def show_budgets():
    # Function to show budgets
    conn = sqlite3.connect('budgets.db')
    cur = conn.cursor()
    cur.execute("SELECT budget_name FROM budgets")
    budgets = cur.fetchone()[0] # [0], [1]... 
    for budget in budgets:
        print(budget)
    conn.commit()
    conn.close()

# Add a new budget
def add_budget(budget_name, budget_amount):
    # Function to add a new budget
    conn = sqlite3.connect('budgets.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO budgets VALUES (?, ?)", (budget_name, budget_amount))
    conn.commit()
    conn.close()

# Delete a budget
def delete_budget(budget_name):
    # Function to delete a budget
    conn = sqlite3.connect('budgets.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM budgets WHERE budget_name = ?", (budget_name))
    conn.commit()
    conn.close()

# Update a budget
def update_budget(budget_name, new_amount):
    # Function to update a budget amount
    conn = sqlite3.connect('budgets.db')
    cur = conn.cursor()
    cur.execute("UPDATE budgets SET budget_amount = ? WHERE budget_name = ?", (new_amount, budget_name))
    conn.commit()
    conn.close()

# User authentication
def authenticate_user(username, password):
    # Function to authenticate a user
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.commit()
    conn.close()
    return user is not None

# Create a new user
def new_user(username, password):
    # Function to create a new user
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO user VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Add a new goal
def add_goal(goal_name, goal_amount):
    # Function to add a new goal
    conn = sqlite3.connect('goals.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO goals VALUES (?, ?)", (goal_name, goal_amount))
    conn.commit()
    conn.close()

# Display goals in database
def show_goals():
    # Function to show goals
    conn = sqlite3.connect('goals.db')
    cur = conn.cursor()
    cur.execute("SELECT goal_name FROM goals")
    goals = cur.fetchone()[0] # [0], [1]... 
    for goal in goals:
        print(goal)
    conn.commit()
    conn.close()

# Delete a goal
def delete_goal(goal_name):
    # Function to delete a goal
    conn = sqlite3.connect('goals.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM goals WHERE goal_name = ?", (goal_name))
    conn.commit()
    conn.close()

# Update a goal
def update_goal(goal_name, new_amount):
    # Function to update a goal amount
    conn = sqlite3.connect('goals.db')
    cur = conn.cursor()
    cur.execute("UPDATE goals SET goal_amount = ? WHERE goal_name = ?", (new_amount, goal_name))
    conn.commit()
    conn.close()

# Note: The above functions are templates and may require additional error handling and validation for production use.
