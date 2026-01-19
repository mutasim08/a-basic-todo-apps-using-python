from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

TODO_FILE = 'todos.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            data = json.load(f)
            # Convert old format (list of strings) to new format (list of dicts)
            if data and len(data) > 0 and isinstance(data[0], str):
                return [{"task": task, "completed": False} for task in data]
            return data
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = load_todos()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    task = data.get('task')
    if not task:
        return jsonify({'error': 'Task required'}), 400
    todos = load_todos()
    todos.append({"task": task, "completed": False})
    save_todos(todos)
    return jsonify({'message': 'Todo added'}), 201

@app.route('/todos/<int:index>', methods=['PUT'])
def update_todo(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        data = request.get_json()
        if 'completed' in data:
            todos[index]['completed'] = data['completed']
        if 'task' in data:
            todos[index]['task'] = data['task']
        save_todos(todos)
        return jsonify({'message': 'Todo updated'})
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/todos/<int:index>', methods=['DELETE'])
def remove_todo(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        save_todos(todos)
        return jsonify({'message': f'Removed: {removed["task"]}'})
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/todos/completed', methods=['DELETE'])
def clear_completed():
    todos = load_todos()
    todos[:] = [todo for todo in todos if not todo['completed']]
    save_todos(todos)
    return jsonify({'message': 'Completed todos cleared'})

if __name__ == '__main__':
    app.run(debug=True)