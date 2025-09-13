import database

class TaskManager:
    """Capa lógica que conecta GUI con base de datos."""

    def __init__(self):
        database.init_db()

    def add_task(self, title, priority="Media"):
        database.add_task(title, priority)

    def get_tasks(self, filter_status=None, search=None):
        return database.get_tasks(filter_status, search)

    def update_task(self, task_id, new_title, new_priority):
        database.update_task(task_id, new_title, new_priority)

    def delete_task(self, task_id):
        database.delete_task(task_id)

    def mark_completed(self, task_id):
        database.mark_completed(task_id)
