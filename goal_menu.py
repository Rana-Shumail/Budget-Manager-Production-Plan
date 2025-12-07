import tkinter as tk
from tkinter import messagebox
from model.goal_inf import insert_goal, Goal
from model.goal_inf import fetch_goals, edit_goal, delete_goal

class Goal_Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width = 720, height = 1200)
        self.root = root
        self.configure(bg="#BEBEBE")
        title = tk.Label(self, text = "Add/Manage Goal", bg = "#BEBEBE", 
                         fg = "#000000", font = ("Averia Serif Libre", 20, "bold"),
                         justify = tk.CENTER)
        title.grid(row = 0, column = 1, columnspan = 5, pady = (10, 20))
        
        self.load_images()
        self.fetched_goals = fetch_goals()
        self.display_info()

        self.instruction_label()
        self.new_goal_button()
        self.main_menu_button()

    # Load and resize trash icon image        
    def load_images(self):
        try:
            self.trash_icon = tk.PhotoImage(file = "img/bin.png")
            self.resized_icon = self.trash_icon.subsample(15, 15)
        except:
            title = 'Image Load Error'
            message = 'Trash icon image could not be loaded. Buttons will be blank.'
            messagebox.showerror(title, message)
            self.resized_icon = tk.PhotoImage() # Empty image as placeholder

    # Create and display goal names and amounts with labels
    def display_info(self):

        self.goal_names = []
        self.goal_amounts = []

        for j, g in enumerate(self.fetched_goals):
            goal_id = g[0]
            next_row = j + 1

            # Show goal names (row = j + 1 since title is row = 0; column 0)
            name_label = tk.Label(self, text = g[1], bg = "#6FFF6F", fg = "#000000", 
                                  font = ("Averia Serif Libre", 14), bd = 2)
            name_label.grid(row = next_row, column = 0, padx = 10, pady = 10, sticky = "nsew")
            name_label.grid_propagate(False)
            self.goal_names.append(name_label)
        
            # Show goal amounts
            amount_label = tk.Label(self, text = g[2], bg = "#0E5200", fg = "#FFFFFF", 
                                    font = ("Averia Serif Libre", 14), bd = 2)
            amount_label.grid(row = next_row, column = 1, padx = 10, pady = 10, sticky = "nsew")
            amount_label.grid_propagate(False)
            self.goal_amounts.append(amount_label)

            # Edit button for each goal
            edit_button = tk.Button(self, text = "Edit", bg = "#01C64C", cursor = "hand2",
                                activebackground = "#01C64C", font = ("Averia Serif Libre", 14),
                                fg = "#000000", command = lambda i = goal_id: self.on_edit(i))
            edit_button.grid(row = next_row, column = 2, padx = 10, pady = 10, sticky = "nsew")

            # Delete button for each goal
            delete_button = tk.Button(self, image = self.resized_icon, bg = "#01C64C", cursor = "hand2",
                            activebackground = "#01C64C", command = lambda i = goal_id: self.on_delete(i))
            delete_button.grid(row = next_row, column = 3, padx = 10, pady = 10, sticky = "nsew")

    def refresh_display(self):
        self.fetched_goals = fetch_goals() 

        # Clear all existing goal-related widgets (rows > 0)
        for widget in self.grid_slaves():

            # Check if widget is below the title (row 0)
            if int(widget.grid_info().get("row", 0)) > 0: 
                widget.grid_forget()
        
        # Redisplay updated goals and buttons
        self.display_info()
        self.instruction_label()
        self.new_goal_button()
        self.main_menu_button()

    def on_delete(self, goal_id):
        try:            
            delete_goal(goal_id)
            title = 'Delete Goal'
            message = 'Goal deleted successfully.'
            messagebox.showinfo(title, message)
            self.refresh_display()
        except:
            title = 'Delete Goal'
            message = 'Goal could not be deleted.'
            messagebox.showerror(title, message)
    
    def on_edit(self, goal_id):
        Edit_Goal_Frame(self.root, self, goal_id)

    def instruction_label(self):
        bullet_char = "\u2022"
        instruction = tk.Label(self, text = f"{bullet_char} Click on \"Edit\" to change the name or amount for your goal."
                               f"\n\n{bullet_char}Click on the trash icon to delete a goal.", 
                                bg = "#BEBEBE", fg = "#000000", font = ("Averia Serif Libre", 14), 
                                bd = 2, justify = tk.LEFT)
        column_span = max(len(self.fetched_goals), 1)
        instruction.grid(row = 1, column = 5, columnspan = column_span, padx = 20, pady = 20, sticky = "nsew")

    def new_goal_button(self):
        new_row = len(self.fetched_goals) + 2
        new = tk.Button(self, text = "Add New Goal", font = ("Averia Serif Libre", 14), 
                        bg = "#000000", cursor = "hand2", fg = "#6FFF6F", activebackground = "#000000", 
                        activeforeground = "#6FFF6F", 
                        command = lambda: Add_Goal_Frame(self.root, self)) # Pass self to refresh after adding
        new.grid(row = new_row, column = 0, padx = 30, pady = 30)

    def back_to_main_menu(self):
        # Import to go back to the main screen when click on Main Menu button
        from client.main_menu import Frame as main_menu_frame

        self.destroy() # Close current frame
        main_menu = main_menu_frame(self.root)
        main_menu.pack(fill="both", expand=True)
    
    def main_menu_button(self):
        new_row = len(self.fetched_goals) + 2
        main_menu = tk.Button(self, text = "Main Menu", font = ("Averia Serif Libre", 14), 
                              bg = "#000000", cursor = "hand2", fg = "#6FFF6F", 
                              activebackground = "#000000", activeforeground = "#6FFF6F", 
                              command = self.back_to_main_menu)
        main_menu.grid(row = new_row, column = 1, padx = 30, pady = 30)

class Add_Goal_Frame(tk.Frame):
    def __init__(self, root, parent_frame): # parent_frame is Goal_Frame
        self.window = tk.Toplevel(root) # Create a new top-level window
        self.window.geometry("550x300")
        self.window.title("Add New Goal")

        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_rowconfigure(0, weight = 1)

        super().__init__(self.window)
        self.root = root
        self.parent_frame = parent_frame # Store reference to the calling Goal_Frame instanc
        self.configure(bg="#919191")

        # Center the window on the screen
        self.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 0) # For Goal Name/Amount
        self.grid_columnconfigure(2, weight = 3) # For entry boxes
        self.grid_columnconfigure(3, weight = 1)

        title = tk.Label(self, text = "Add New Goal", bg = "#919191", 
                         fg = "#000000", font = ("Averia Serif Libre", 16, "bold"))
        title.grid(row = 0, column = 0, columnspan = 4, pady = (10, 20), sticky = "ew")

        # Display fields and buttons
        self.goal_fields()
        self.button_add() 
        self.cancel_button()

        # Push content up if resized vertically
        self.window.transient(root) # Set window on top of Goal Menu
        self.window.grab_set() # Modal behavior
        root.wait_window(self.window) # Pause execution until Toplevel is closed 
        
    def goal_fields(self):
        name_label = tk.Label(self, text = "Goal Name:", bg = "#919191", fg = "#000000", 
                              font = ("Averia Serif Libre", 14))
        name_label.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = "ew")

        amount_label = tk.Label(self, text = "Goal Amount:", bg = "#919191", fg = "#000000", 
                                font = ("Averia Serif Libre", 14))
        amount_label.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "e")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = "ew")
        

    def button_add(self):
        add_button = tk.Button(self, text = "Add Goal", font = ("Averia Serif Libre", 14), 
                               bg = "#919191", cursor = "hand2", activebackground = "#919191", 
                               command = self.on_add)
        add_button.grid(row = 3, column = 2, padx = 20, pady = 20, sticky = "e")
    
    def cancel_button(self):
        cancel_button = tk.Button(self, text = "Cancel", font = ("Averia Serif Libre", 14), 
                                  bg = "#919191", cursor = "hand2", activebackground = "#919191", 
                                  command = self.window.destroy)
        cancel_button.grid(row = 3, column = 1, padx = 20, pady = 20, sticky = "w")

    def on_add(self):
        goal_name = self.name_entry.get().strip()
        goal_amount_str = self.amount_entry.get().strip()

        # Validate that fields are not empty
        if not goal_name or not goal_amount_str:
            title = "Input Error"
            message = "Please fill in all fields."
            messagebox.showerror(title, message)
            return

        # Validate goal_amount is a positive number
        try:
            goal_amount = float(goal_amount_str)
            if goal_amount < 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            title = "Input Error"
            message = "Please enter a valid positive number for the goal amount."
            messagebox.showerror(title, message)
            return
        
        # Insert the new goal into the database
        try:
            new_goal = Goal(goal_name, goal_amount)
            insert_goal(new_goal)
            title = "Add Goal"
            message = f"Goal {goal_name} added successfully."
            messagebox.showinfo(title, message)
            self.parent_frame.refresh_display() # Refresh the parent Goal_Frame display
            self.window.destroy() # Close the add goal window
        except:
            title = "Add Goal"
            message = "Goal could not be added."
            messagebox.showerror(title, message)

class Edit_Goal_Frame(tk.Frame):
    def __init__(self, root, parent_frame, goal_id):
        self.window = tk.Toplevel(root)
        self.window.geometry("600x400")
        self.window.title("Edit Goal")

        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_rowconfigure(0, weight = 1)

        super().__init__(self.window)
        self.configure(bg = "#919191")
        self.goal_id = goal_id # Store the ID of the goal being edited
        self.parent_frame = parent_frame
        self.root = root

        self.current_goal_data = self.fetch_current_goal_data(goal_id)
        if not self.current_goal_data:
            title = "Edit Goal"
            message = "Could not fetch goal data. Window will close."
            messagebox.showerror(title, message)
            self.window.destroy()
            return
                               
        self.grid(row = 0, column = 0, sticky = "nsew", padx=20, pady=20)
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 0) # For Goal Name/Amount info
        self.grid_columnconfigure(2, weight = 3) # For fields/entry boxes
        self.grid_columnconfigure(3, weight = 1)
        
        title = tk.Label(self, text = "Edit Goal", bg = "#919191", fg = "#000000",
                          font = ("Averia Serif Libre", 14))
        title.grid(row = 0, column = 0, columnspan = 4, pady = (10, 20), sticky= "ew")

        self.display_current_goal()
        self.new_goal_fields()
        self.button_save()
        self.cancel_button()

        # Set column weights for proper resizing
        self.grid_columnconfigure(6, weight = 1)

        self.window.transient(root)
        self.window.grab_set()
        root.wait_window(self.window)

        # Fetch current goal data from database
    def fetch_current_goal_data(self, goal_id):
        goals = fetch_goals()
        for g in goals:
            if g[0] == goal_id:
                return g # Return the goal tuple
        return None
    
    def display_current_goal(self):

        current_name = self.current_goal_data[1]
        current_amount = self.current_goal_data[2]

        # Display current goal name
        current_name_label = tk.Label(self, text = "Current name:", bg = "#919191", 
                                      fg = "#000000", font = ("Averia Serif Libre", 14))
        current_name_label.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "e")

        current_name = tk.Label(self, text = current_name, bg = "#919191", 
                                fg = "#000000", font = ("Averia Serif Libre", 14), bd = 2)
        current_name.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = "ew")

        #Display current goal amount
        current_amount_label = tk.Label(self, text = "Current amount:", bg = "#919191", 
                                        fg = "#000000", font = ("Averia Serif Libre", 14), bd = 2)
        current_amount_label.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "e")

        current_amount = tk.Label(self, text = current_amount, bg = "#919191", 
                                  fg = "#000000", font = ("Averia Serif Libre", 14), bd = 2)
        current_amount.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = "ew")

    def new_goal_fields(self):
        # New goal name
        new_name_label = tk.Label(self, text = "New name:", bg = "#919191", 
                                  fg = "#000000", font = ("Averia Serif Libre", 14))
        new_name_label.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = "ew")
        self.new_name_entry = tk.Entry(self)
        self.new_name_entry.insert(0, self.current_goal_data[1])
        self.new_name_entry.grid(row = 3, column = 2, padx = 10, pady = 10, sticky = "ew")

        # New goal amount
        new_amount_label = tk.Label(self, text = "New amount:", bg = "#919191", 
                                    fg = "#000000", font = ("Averia Serif Libre", 14))
        new_amount_label.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = "e")
        self.new_amount_entry = tk.Entry(self)
        self.new_amount_entry.insert(0, self.current_goal_data[2])
        self.new_amount_entry.grid(row = 4, column = 2, padx = 10, pady = 10, sticky = "ew")

    def button_save(self):
        save_button = tk.Button(self, text = "Save", font = ("Averia Serif Libre", 14), 
                                bg = "#919191", cursor = "hand2", activebackground = "#919191", 
                                command = self.on_save)
        save_button.grid(row = 5, column = 2, padx = 20, pady = 20, sticky = "e")
    
    def cancel_button(self):
        cancel_button = tk.Button(self, text = "Cancel", font = ("Averia Serif Libre", 14), 
                                  bg = "#919191", cursor = "hand2", activebackground = "#919191", 
                                  command = self.window.destroy)
        cancel_button.grid(row = 5, column = 1, padx = 20, pady = 20, sticky = "w")

    def on_save(self):
        new_name = self.new_name_entry.get().strip()
        new_amount_str = self.new_amount_entry.get().strip()

        # Validate that fields are not empty
        if not new_name or not new_amount_str:
            title = "Input Error"
            message = "Fields cannot be empty."
            messagebox.showerror(title, message)
            return

        # Validate new_amount is a positive number
        try:
            new_amount = float(new_amount_str)
            if new_amount < 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            title = "Input Error"
            message = "Please enter a valid positive number for the goal amount."
            messagebox.showerror(title, message)
            return
        
        # Insert the updated goal into the database
        try:
            updated_goal = Goal(new_name, new_amount)
            edit_goal(updated_goal, self.goal_id)

            title = "Edit Goal"
            message = f"Goal {new_name} edited successfully."
            messagebox.showinfo(title, message)
            self.parent_frame.refresh_display() # Refresh the parent Goal_Frame display
            self.window.destroy() # Close the Edit goal window
        except:
            title = "Edit Goal"
            message = "Goal could not be edited."
            messagebox.showerror(title, message)
