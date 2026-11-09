from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
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

def load_tasks():
    loaded_tasks = []

    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for task in data:
            task1 = Task(task["name"], task["done"], task["priority"], task.get("id"))
            loaded_tasks.append(task1)

    except FileNotFoundError:
        pass
    return loaded_tasks

def save_tasks(tasks_list, verbose=True):
    data = []
    for task in tasks_list:
        data.append({
            "name": task.name,
            "done": task.done,
            "priority": task.priority,
            "id": task.id
        })
    with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False , indent=2)

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
    if task_name:
        current_tasks = load_tasks()
        new_task = Task(task_name)
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

if __name__ == "__main__":
    app.run(debug=True)
