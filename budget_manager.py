import tkinter as tk
from client.gui import Frame

def main():
    root = tk.Tk()
    root.title("Buddbuddy")
    root.configure(bg = "#BEBEBE")

    app_frame = Frame(root = root)

    app_frame.mainloop()


if __name__ == "__main__":
    main()