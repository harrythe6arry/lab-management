from flask import Flask, request, jsonify, Blueprint, render_template

from Utils import tasks

app = Flask(__name__)

tasks_routes = Blueprint("tasks_routes", __name__)

@tasks_routes.route('/tasks', methods=['GET'])
def fetch_tasks():
    """Fetch all tasks."""
    task = tasks.get_all_tasks()
    return render_template('tasks.html', task_data=task)

@tasks_routes.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    """Add a new task."""
    name = request.form.get('name')
    due_date = request.form.get('due_date')
    status = request.form.get('status')
    assigned_to = request.form.get('assigned_to')

    try:
        new_task_id = tasks.add_task(name, due_date, status, assigned_to)
        return jsonify({'message': 'Task added successfully', 'task_id': new_task_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


