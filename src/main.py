import customtkinter as ctk
from gui import TaskApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = TaskApp(root)
    root.mainloop()
