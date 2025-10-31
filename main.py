import tkinter as tk
from goals_db import create_table
from ui import render_goals

# Create the goals table if it doesn't exist
create_table()

# Initialize the main window
root = tk.Tk()
root.title("Goal Manager")
root.configure(bg="#1e1e1e")

# Create a container for goal entries
goals_container = tk.Frame(root, bg="#1e1e1e")
goals_container.pack(padx=20, pady=20)

# Render all goals into the UI
render_goals(goals_container)

# Start the Tkinter event loop
root.mainloop()
