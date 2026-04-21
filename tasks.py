import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: [{task['id']}] {title}")


def list_tasks(show_all=False):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        if not show_all and task["done"]:
            continue
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['title']}")


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Completed: {task['title']}")
            return
    print(f"Task {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == original_count:
        print(f"Task {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Deleted task {task_id}.")


def search_tasks(query):
    tasks = load_tasks()
    results = [t for t in tasks if query.lower() in t["title"].lower()]
    if not results:
        print(f"No tasks matching '{query}'.")
        return
    for task in results:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['title']}")
