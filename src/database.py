import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/tasks.db")

def init_db():
    """Crea la base de datos y la tabla si no existen."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT CHECK(status IN ('pendiente','completada')) NOT NULL DEFAULT 'pendiente',
            priority TEXT CHECK(priority IN ('Alta','Media','Baja')) NOT NULL DEFAULT 'Media'
        )
    ''')
    conn.commit()
    conn.close()

def add_task(title, priority="Media"):
    """Agrega una nueva tarea con título y prioridad."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, status, priority) VALUES (?, 'pendiente', ?)", (title, priority))
    conn.commit()
    conn.close()

def get_tasks(filter_status=None, search=None):
    """Obtiene todas las tareas, con filtros opcionales."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT id, title, status, priority FROM tasks WHERE 1=1"
    params = []

    if filter_status:
        query += " AND status = ?"
        params.append(filter_status)

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_task(task_id, new_title, new_priority):
    """Actualiza título y prioridad de una tarea."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ?, priority = ? WHERE id = ?", (new_title, new_priority, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Elimina una tarea por ID."""
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
