import sqlite3
import os

# Definimos la ruta donde se guardará la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/tasks.db")

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Crea carpeta /data si no existe
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,        -- identificador único
            title TEXT NOT NULL,                         -- título de la tarea
            status TEXT CHECK(status IN ('pendiente','completada')) NOT NULL DEFAULT 'pendiente'
        )
    ''')
    conn.commit()
    conn.close()

def add_task(title):
    """Agrega una nueva tarea con estado pendiente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, status) VALUES (?, 'pendiente')", (title,))
    conn.commit()
    conn.close()

def get_tasks():
    """Obtiene todas las tareas almacenadas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_task(task_id, new_title):
    """Actualiza el título de una tarea existente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Elimina una tarea por su ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def mark_completed(task_id):
    """Marca una tarea como completada."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completada' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
