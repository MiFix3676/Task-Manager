from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import uuid

class Task:
    def __init__(self, name, done=False, priority="Обычный", id = None):
        self.name = name
        self.done = done
        self.priority = priority
        self.id = id if id else str(uuid.uuid4())

    def mark_task(self):
        self.done = not self.done

    def set_priority(self, new_priority):
        self.priority = new_priority

def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    name TEXT,
    done INTEGER,
    priority TEXT
    )''')

    conn.commit()
    conn.close()

def load_tasks():
    loaded_tasks = []

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    for row in rows:
        task1 = Task(row[1], row[2], row[3], row[0])
        loaded_tasks.append(task1)

    return loaded_tasks

def save_tasks(tasks_list):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("delete from tasks")
    for task in tasks_list:
        cursor.execute('''insert into tasks (name, done, priority, id) values (?, ?, ?, ?)''',
                       (task.name, task.done, task.priority, task.id))
    conn.commit()
    conn.close()

app = Flask(__name__)
@app.route("/")
def index():
    return "привет мир"

@app.route("/tasks")
def tasks():
    return render_template("tasks.html", tasks=load_tasks())

@app.route("/about")
def about():
    return "Это мой первый сайт"

@app.route("/add", methods=["POST"])
def add():
    task_name = request.form.get("task_name")
    task_priority = request.form.get("task_priority")
    if task_name:
        current_tasks = load_tasks()
        new_task = Task(task_name, priority=task_priority)
        current_tasks.append(new_task)
        save_tasks(current_tasks)
        return jsonify({"id": new_task.id})

@app.route("/delete", methods=["POST"])
def delete():
    id_str = request.form.get("task_id")
    tasks = load_tasks()
    for task in tasks:
        if task.id == id_str:
            tasks.remove(task)
            save_tasks(tasks)
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "massage": "Такой задачи нет"})

@app.route("/toggle", methods=["POST"])
def toggle():
    id_str = request.form.get("task_id")
    tasks = load_tasks()
    for task in tasks:
        if task.id == id_str:
            task.mark_task()
            save_tasks(tasks)
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "Такой задачи нет"})

@app.route("/change_priority", methods=["POST"])
def change_priority():
    id_str = request.form.get("task_id")
    new_priority = request.form.get("priority")
    tasks = load_tasks()
    for task in tasks:
        if task.id == id_str:
            task.priority = new_priority
            save_tasks(tasks)
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "Такой задачи нет"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
