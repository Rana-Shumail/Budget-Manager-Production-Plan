import tkinter as tk
from client.main_menu import Frame as main_menu
from client.goal_menu import Goal_Frame
#from model.budget_inf import create_budget_table
#from model.goal_inf import create_goal_table

def main():
    #create_goal_table()
    #create_budget_table()

    root = tk.Tk()
    root.title("Buddbuddy")
    root.configure(bg = "#BEBEBE")

    app_frame = main_menu(root = root)

    app_frame.pack(fill = "both", expand = True)

    root.mainloop()


if __name__ == "__main__":
    main()
