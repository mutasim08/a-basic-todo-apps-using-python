# Basic Todo App

A simple todo application with both command-line and web interfaces, built with Python and Flask.

## Features

- Add new todos
- List all todos
- Remove todos
- Persistent storage using JSON
- Command-line interface (CLI)
- Web interface with REST API

## Usage

### Command-line Version

Run the CLI app:

```bash
python todo.py
```

Follow the menu options to add, list, or remove todos.

### Web Version

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web server:
```bash
python app.py
```

3. Open your browser and go to `http://127.0.0.1:5000/`

The web interface allows you to add and remove todos interactively.

## Requirements

- Python 3.x
- Flask (for web version)

## API Endpoints (Web Version)

- `GET /todos`: Retrieve all todos
- `POST /todos`: Add a new todo (JSON body: `{"task": "your task"}`)
- `DELETE /todos/<index>`: Remove todo by index

## Troubleshooting

- Ensure Python is installed and accessible
- For web version, install Flask: `pip install flask`
- Run commands in the directory containing the scripts
- Todos are automatically saved to `todos.json` in the same directory
- If you encounter issues, check that the directory is writable
- Web server runs on port 5000 by default