import tkinter as tk
from tkinter import messagebox, simpledialog
from task_manager import TaskManager

class TaskApp:
    """Clase que maneja la interfaz gráfica del gestor de tareas usando Tkinter."""

    def __init__(self, root):
        # Instanciamos el gestor de tareas (capa lógica)
        self.manager = TaskManager()
        self.root = root
        self.root.title("Gestor de Tareas")

        # Campo de texto para ingresar nuevas tareas
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        # Botón para agregar tareas
        self.add_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack()

        # Lista donde se mostrarán todas las tareas
        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(pady=10)

        # Botones de acción
        self.edit_button = tk.Button(root, text="Editar", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.complete_button = tk.Button(root, text="Marcar Completada", command=self.mark_completed)
        self.complete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Cargamos las tareas al iniciar
        self.refresh_tasks()

    def add_task(self):
        """Agrega una nueva tarea al presionar el botón."""
        title = self.entry.get().strip()
        if title:
            self.manager.add_task(title)   # Guardamos en la base de datos
            self.entry.delete(0, tk.END)   # Limpiamos la caja de texto
            self.refresh_tasks()           # Refrescamos la lista
        else:
            messagebox.showwarning("Error", "El título no puede estar vacío")

    def refresh_tasks(self):
        """Actualiza el listado de tareas en pantalla."""
        self.listbox.delete(0, tk.END)     # Limpiamos lista
        tasks = self.manager.get_tasks()   # Obtenemos desde la base
        for task in tasks:
            display = f"[{task[2]}] {task[1]} (ID: {task[0]})"
            self.listbox.insert(tk.END, display)

    def get_selected_task_id(self):
        """Devuelve el ID de la tarea seleccionada en la lista."""
        try:
            selection = self.listbox.get(self.listbox.curselection())
            return int(selection.split("ID: ")[1].replace(")", ""))
        except:
            return None

    def edit_task(self):
        """Edita el título de una tarea seleccionada."""
        task_id = self.get_selected_task_id()
        if task_id:
            new_title = simpledialog.askstring("Editar", "Nuevo título:")
            if new_title:
                self.manager.update_task(task_id, new_title)
                self.refresh_tasks()
        else:
            messagebox.showwarning("Error", "Selecciona una tarea")

    def delete_task(self):
        """Elimina una tarea seleccionada."""
        task_id = self.get_selected_task_id()
        if task_id:
            confirm = messagebox.askyesno("Confirmar", "¿Eliminar la tarea?")
            if confirm:
                self.manager.delete_task(task_id)
                self.refresh_tasks()
        else:
            messagebox.showwarning("Error", "Selecciona una tarea")

    def mark_completed(self):
        """Marca como completada la tarea seleccionada."""
        task_id = self.get_selected_task_id()
        if task_id:
            self.manager.mark_completed(task_id)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Error", "Selecciona una tarea")
