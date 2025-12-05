import tkinter as tk
from model.budget_inf import fetch_budgets
from model.goal_inf import fetch_goals

# Define a Frame class to encapsulate the budget and goal frames
class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width=800, height=600)
        self.root = root
        self.configure(bg="#BEBEBE")

        self.fetched_budgets = fetch_budgets()
        self.fetched_goals = fetch_goals()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.display_content()        

    # Method to create and display budget and goal frames
    def display_content(self):

        # Frame for displays
        wrapper_frame = tk.Frame(self, bg="#BEBEBE")
        wrapper_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        wrapper_frame.grid_columnconfigure(0, weight=1)
        wrapper_frame.grid_rowconfigure(999, weight = 1) # Pushes content up

        self.budget_frames = []
        self.goal_frames = []

        # Check if tables have data
        has_data = bool(self.fetched_budgets or self.fetched_goals)
        current_row = 0

        if not has_data:
        # Placeholder if tables are empty
            placeholder_text = ("Welcome to Buddbuddy!\n\n"
                                "You have no budgets or goals yet.\n"
                                "Select one option to get started.")
            
            placeholder_label = tk.Label(wrapper_frame, text = placeholder_text, bg = "#BEBEBE", fg = "#000000",
                                         font = ("Averia Serif Libre", 14), justify = tk.CENTER)
            placeholder_label.grid(row = 0, column = 0, padx = 30, pady = 50, sticky = "nsew")
        else:

            # Budget Frame
            for i, b in enumerate(self.fetched_budgets):
                frame_budget1 = tk.Frame(wrapper_frame, bg = "#FFFFFF", bd = 3, relief = tk.RAISED, width = 250, height = 80)
                frame_budget1.grid(row = current_row, column = 0, padx = 10, pady = 10, sticky = "nsew")
                frame_budget1.grid_propagate(False)
                frame_budget1.grid_columnconfigure(0, weight = 1)

                # b[1] is name, b[2] is amount
                tk.Label(frame_budget1, text = f"Budget: {b[1]}", bg = "#0E5200", fg="#FFFFFF").grid(row=0, column=0)
                tk.Label(frame_budget1, text = f"${b[2]}", bg = "#0E5200", fg="#FFFFFF").grid(row=1, column=0)

                self.budget_frames.append(frame_budget1)
                current_row += 1
                
            # Goal Frame
            for j, g in enumerate(self.fetched_goals):
                frame_goal1 = tk.Frame(wrapper_frame, bg = "#FFFFFF", bd = 2, relief = tk.RAISED, width = 250, height = 80)
                frame_goal1.grid(row = current_row, column = 0, padx = 10, pady = 10, sticky = "nsew")
                frame_goal1.grid_propagate(False)
                frame_goal1.grid_columnconfigure(0, weight = 1)

                # g[1] is name, g[2] is amount
                tk.Label(frame_goal1, text = f"Goal: {g[1]}", bg = "#0E5200", fg="#FFFFFF").grid(row=0, column=0)
                tk.Label(frame_goal1, text = f"Target: ${g[2]}", bg = "#0E5200", fg="#FFFFFF").grid(row=1, column=0)

                self.goal_frames.append(frame_goal1)
                current_row += 1
                wrapper_frame.grid_rowconfigure(current_row, weight = 1)

        # Place buttons in the right side of the frame
        self.option_buttons()

    def option_buttons(self):
        
        buttons_frame = tk.Frame(self, bg = "#919191")
        buttons_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nsew")

        buttons_frame.grid_columnconfigure(0, weight = 1)

        #Center buttons one on top of the other
        buttons_frame.grid_rowconfigure(0, weight = 1)
        buttons_frame.grid_rowconfigure(3, weight = 1)

        self.create_budget_button(buttons_frame).grid(row = 1, column = 0, padx = 10, pady = 30, sticky = "ew")
        self.manage_goal_button(buttons_frame).grid(row = 2, column = 0, padx = 10, pady = 30, sticky = "ew")

    def create_budget_button(self, parent_frame):
        return tk.Button(parent_frame, text = "Create/Manage Budget", font = ("Averia Serif Libre", 16, "bold"), bg = "#6FFF6F", cursor = "hand2",
                                  fg = "#000000", activebackground = "#6FFF6F", command = lambda: print("This goes to Budget Screen."))
    
    def manage_goal_button(self, parent_frame):
        return tk.Button(parent_frame, text = "Add/Manage Goal", font = ("Averia Serif Libre", 16, "bold"), bg = "#000000", cursor = "hand2",
                                  fg = "#6FFF6F", activebackground = "#000000", command = self.to_goal_menu)

    def to_goal_menu(self):
        # Import to access Goal's main menu when click on Add/Manage Goal button
        from client.goal_menu import Goal_Frame

        self.destroy()

        # Create the Goal_Frame class onto the root
        goal_menu = Goal_Frame(self.root)
        goal_menu.pack(fill = "both", expand = True)