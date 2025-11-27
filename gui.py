import tkinter as tk
from model.budget_inf import fetch_budgets
from model.goal_inf import fetch_goals

# Define a Frame class to encapsulate the budget and goal frames
class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width=800, height=600)
        self.root = root
        self.configure(bg="#BEBEBE")
        self.pack(padx=10, pady=10)

        self.display_frame()

    # Method to create and display budget and goal frames
    def display_frame(self):

        self.fetched_budgets = fetch_budgets()
        self.fetched_goals = fetch_goals()

        self.budget_frames = []
        self.goal_frames = []

        # Budget Frame
        for i, b in enumerate(self.fetched_budgets):
            frame_budget1 = tk.Frame(self, bg = "#FFFFFF", bd = 3, width = 20, height = 20)
            frame_budget1.grid(row=0, column=i, padx = 10, pady = 10, sticky = "nsew")
            frame_budget1.grid_propagate(False)

            # b[1] is name, b[2] is amount
            tk.Label(frame_budget1, text = b[1], bg = "#0E5200", fg="#FFFFFF").grid(row=0, column=0)
            tk.Label(frame_budget1, text = b[2], bg = "#0E5200", fg="#FFFFFF").grid(row=1, column=0)

            self.budget_frames.append(frame_budget1)
            
        # Goal Frame
        for j, g in enumerate(self.fetched_goals):
            frame_goal1 = tk.Frame(self, bg = "#FFFFFF", bd = 2, width = 20, height = 20)
            frame_goal1.grid(row = 1, column = j, padx = 10, pady = 10, sticky = "nsew")
            frame_goal1.grid_propagate(False)

            # g[1] is name, g[2] is amount
            tk.Label(frame_goal1, text = g[1], bg = "#0E5200", fg="#FFFFFF").grid(row=0, column=0)
            tk.Label(frame_goal1, text = g[2], bg = "#0E5200", fg="#FFFFFF").grid(row=1, column=0)

            self.goal_frames.append(frame_goal1)