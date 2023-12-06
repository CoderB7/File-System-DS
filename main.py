import tkinter as tk
from tree_UI import FileSystemExplorer

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("620x400")

    file_system = FileSystemExplorer()

    root.mainloop()

