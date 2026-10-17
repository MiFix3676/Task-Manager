from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)
