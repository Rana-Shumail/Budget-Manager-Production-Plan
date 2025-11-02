# THIS IS JUST A SAMPLE OF THE UI CODE. THIS IS NOT THE FINAL UI FOR JUST A TRASH ICON.
import tkinter as tk
from database import fetch_goals, delete_goal

def render_goals(container):
    for goal in fetch_goals():
        goal_id, name, amount = goal
        frame = tk.Frame(container, bg="#1e1e1e")
        
        tk.Label(frame, text=name, fg="#b6ff9c", bg="#1e1e1e").pack(side="left", padx=10)
        tk.Label(frame, text=f"${amount:.2f}", fg="#b6ff9c", bg="#1e1e1e").pack(side="left", padx=10)
        
        trash_icon = tk.PhotoImage(file="trash_icon.png")
        delete_btn = tk.Button(
            frame,
            image=trash_icon,
            command=lambda gid=goal_id, f=frame: (delete_goal(gid), f.destroy()),
            bg="#1e1e1e",
            activebackground="#1e1e1e",
            borderwidth=0
        )
        delete_btn.image = trash_icon
        delete_btn.pack(side="right", padx=10)
        
        frame.pack(pady=5, fill="x")
