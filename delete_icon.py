import tkinter as tk
from tkinter import messagebox
from model.goal_inf import delete_goal
from model.goal_inf import Goal

root = tk.Tk()

trash_icon = tk.PhotoImage(file = "UI/img/bin.png")
resized_icon = trash_icon.subsample(15, 15)
delete_button = tk.Button(root, image = resized_icon, bg = "#01C64C", 
                          activebackground = "#01C64C", command = lambda : on_delete())
delete_button.pack()

def on_delete(self):
    try:
        id_goal = self.get_selected_goal_id()  # Assume this method retrieves the selected goal's ID
        delete_goal(id_goal)
        title = 'Delete Goal'
        message = 'Table Goal created.'
        messagebox.showinfo(title, message)
    except:
        title = 'Delete Goal'
        message = 'Goal could not be deleted.'
        messagebox.showerror(title, message)


root.mainloop()