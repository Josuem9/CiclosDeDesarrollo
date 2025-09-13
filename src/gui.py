import customtkinter as ctk
from tkinter import messagebox, simpledialog
from task_manager import TaskManager

class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Gestor de Tareas - Versión 2")

        # Configuración de tema
        ctk.set_appearance_mode("system")  # "dark", "light", "system"
        ctk.set_default_color_theme("blue")

        # Frame principal
        self.frame = ctk.CTkFrame(root, corner_radius=15)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Entrada de nueva tarea
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Escribe una nueva tarea...")
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Selección de prioridad
        self.priority_var = ctk.StringVar(value="Media")
        self.priority_menu = ctk.CTkOptionMenu(self.frame, variable=self.priority_var, values=["Alta", "Media", "Baja"])
        self.priority_menu.grid(row=0, column=1, padx=5, pady=5)

        # Botón para agregar
        self.add_button = ctk.CTkButton(self.frame, text="Agregar", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(self.frame, placeholder_text="Buscar...")
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.search_button = ctk.CTkButton(self.frame, text="Buscar", command=self.search_task)
        self.search_button.grid(row=1, column=2, padx=5, pady=5)

        # Filtro por estado
        self.filter_var = ctk.StringVar(value="Todos")
        self.filter_menu = ctk.CTkOptionMenu(self.frame, variable=self.filter_var, values=["Todos", "pendiente", "completada"], command=lambda _: self.refresh_tasks())
        self.filter_menu.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Lista de tareas
        self.listbox = ctk.CTkTextbox(self.frame, width=600, height=300)
        self.listbox.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        # Botones de acción
        self.edit_button = ctk.CTkButton(self.frame, text="Editar", command=self.edit_task)
        self.edit_button.grid(row=4, column=0, padx=5, pady=5)

        self.delete_button = ctk.CTkButton(self.frame, text="Eliminar", command=self.delete_task)
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

        self.complete_button = ctk.CTkButton(self.frame, text="Completar", command=self.mark_completed)
        self.complete_button.grid(row=4, column=2, padx=5, pady=5)

        # Ajustar columnas
        self.frame.grid_columnconfigure(0, weight=1)

        # Cargar tareas
        self.refresh_tasks()

    def add_task(self):
        title = self.entry.get().strip()
        priority = self.priority_var.get()
        if title:
            self.manager.add_task(title, priority)
            self.entry.delete(0, "end")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Error", "El título no puede estar vacío")

    def refresh_tasks(self):
        """Muestra todas las tareas en el cuadro de texto."""
        self.listbox.delete("1.0", "end")
        filter_status = None if self.filter_var.get() == "Todos" else self.filter_var.get()
        tasks = self.manager.get_tasks(filter_status)
        for task in tasks:
            display = f"ID: {task[0]} | {task[1]} | Estado: {task[2]} | Prioridad: {task[3]}\n"
            self.listbox.insert("end", display)

    def get_selected_task_id(self):
        """Pide al usuario el ID de la tarea a modificar/eliminar."""
        task_id = simpledialog.askinteger("Seleccionar tarea", "Introduce el ID de la tarea:")
        return task_id

    def edit_task(self):
        task_id = self.get_selected_task_id()
        if task_id:
            new_title = simpledialog.askstring("Editar", "Nuevo título:")
            new_priority = simpledialog.askstring("Editar", "Nueva prioridad (Alta/Media/Baja):", initialvalue="Media")
            if new_title and new_priority in ["Alta", "Media", "Baja"]:
                self.manager.update_task(task_id, new_title, new_priority)
                self.refresh_tasks()
        else:
            messagebox.showwarning("Error", "Debes indicar un ID válido")

    def delete_task(self):
        task_id = self.get_selected_task_id()
        if task_id:
            confirm = messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?")
            if confirm:
                self.manager.delete_task(task_id)
                self.refresh_tasks()

    def mark_completed(self):
        task_id = self.get_selected_task_id()
        if task_id:
            self.manager.mark_completed(task_id)
            self.refresh_tasks()

    def search_task(self):
        """Busca tareas por palabra clave."""
        query = self.search_entry.get().strip()
        self.listbox.delete("1.0", "end")
        tasks = self.manager.get_tasks(search=query)
        for task in tasks:
            display = f"ID: {task[0]} | {task[1]} | Estado: {task[2]} | Prioridad: {task[3]}\n"
            self.listbox.insert("end", display)
