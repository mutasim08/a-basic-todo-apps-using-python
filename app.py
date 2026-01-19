from flask import Flask, request, jsonify, render_template, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

TODOS_FILE = 'todos.json'
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            data = json.load(f)
            if data and len(data) > 0 and isinstance(data[0], str):
                return [{"task": task, "completed": False, "date": datetime.now().strftime('%Y-%m-%d')} for task in data]
            return data
    return []

def save_todos(todos):
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html')
    return render_template('auth.html')

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'error': 'All fields required'}), 400
    
    users = load_users()
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    users[username] = {
        'password': password,
        'email': email,
        'name': username,
        'avatar': '👤',
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    save_users(users)
    session['username'] = username
    return jsonify({'message': 'Signup successful', 'username': username}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    users = load_users()
    if username not in users or users[username]['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['username'] = username
    return jsonify({'message': 'Login successful', 'username': username}), 200

@app.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/profile', methods=['GET'])
def get_profile():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    users = load_users()
    if username not in users:
        return jsonify({'error': 'User not found'}), 404
    
    user = users[username].copy()
    user['username'] = username
    return jsonify(user), 200

@app.route('/profile', methods=['PUT'])
def update_profile():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    users = load_users()
    
    if 'name' in data:
        users[username]['name'] = data['name']
    if 'email' in data:
        users[username]['email'] = data['email']
    if 'avatar' in data:
        users[username]['avatar'] = data['avatar']
    
    save_users(users)
    return jsonify({'message': 'Profile updated'}), 200

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    todos = load_todos()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    task = data.get('task')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if not task:
        return jsonify({'error': 'Task required'}), 400
    todos = load_todos()
    todos.append({"task": task, "completed": False, "date": date})
    save_todos(todos)
    return jsonify({'message': 'Todo added'}), 201

@app.route('/todos/<int:index>', methods=['PUT'])
def update_todo(index):
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
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
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    todos = load_todos()
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        saved_todos = [todo for todo in todos if isinstance(todo, dict)]
        save_todos(saved_todos)
        return jsonify({'message': f'Removed: {removed.get("task", "Task")}'})
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/todos/completed', methods=['DELETE'])
def clear_completed():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    todos = load_todos()
    todos[:] = [todo for todo in todos if not todo.get('completed', False)]
    save_todos(todos)
    return jsonify({'message': 'Completed todos cleared'})

if __name__ == '__main__':
    app.run(debug=True)