import database

class TaskManager:
    """Clase que sirve como capa intermedia entre la base de datos y la interfaz gráfica."""

    def __init__(self):
        # Inicializa la base de datos al crear el objeto
        database.init_db()
    
    #Agrega una nueva tarea a la base de datos
    def add_task(self, title): 
        database.add_task(title)
    # Obtiene todas las tareas registradas en la base de datos.
    def get_tasks(self):
        return database.get_tasks()
    #Modifica el título de una tarea existente.
    def update_task(self, task_id, new_title):
        database.update_task(task_id, new_title)

    # Elimina una tarea de la base de datos según su ID.
    def delete_task(self, task_id):
        database.delete_task(task_id)

    #  Marca una tarea como 'completada'.
    def mark_completed(self, task_id):
        database.mark_completed(task_id)
