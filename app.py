from flask import Flask, render_template, request, redirect, url_for
import json

class Task:
    def __init__(self, name, done=False, priority="Обычный"):
        self.name = name
        self.done = done
        self.priority = priority

    def mark_task(self):
        self.done = True

    def set_priority(self, new_priority):
        self.priority = new_priority

def load_tasks():
    loaded_tasks = []

    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for task in data:
            task1 = Task(task["name"], task["done"], task["priority"])
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
            "priority": task.priority
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
    task = request.form.get("task_name")
    if task:
        current_tasks = load_tasks()
        task = Task(task)
        current_tasks.append(task)
        save_tasks(current_tasks)
    return redirect(url_for("tasks"))

@app.route("/delete", methods=["POST"])
def delete():
    index_str = request.form.get("task_index")
    index = int(index_str)
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)
    return redirect(url_for("tasks"))


if __name__ == "__main__":
    app.run(debug=True)
