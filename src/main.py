import tkinter as tk
from gui import TaskApp

if __name__ == "__main__":
    # Inicia la aplicación gráfica
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
