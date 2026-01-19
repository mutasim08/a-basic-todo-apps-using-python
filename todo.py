import json
import os

TODO_FILE = 'todos.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f)

def add_todo(todos, task):
    todos.append(task)
    save_todos(todos)

def list_todos(todos):
    if not todos:
        print("No todos.")
    else:
        for i, task in enumerate(todos, 1):
            print(f"{i}. {task}")

def remove_todo(todos, index):
    if 1 <= index <= len(todos):
        removed = todos.pop(index - 1)
        save_todos(todos)
        print(f"Removed: {removed}")
    else:
        print("Invalid index.")

def main():
    todos = load_todos()
    while True:
        print("\n1. Add todo")
        print("2. List todos")
        print("3. Remove todo")
        print("4. Quit")
        choice = input("Choose: ")
        if choice == '1':
            task = input("Task: ")
            add_todo(todos, task)
        elif choice == '2':
            list_todos(todos)
        elif choice == '3':
            try:
                index = int(input("Index to remove: "))
                remove_todo(todos, index)
            except ValueError:
                print("Please enter a number.")
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()