from datetime import datetime, timezone
from flask import request, jsonify, Blueprint, render_template

import app.service.user
from app.routes import auth
from app.routes.auth import user_login_required
from app.service import tasks, timezone

tasks_routes = Blueprint("tasks_routes", __name__)


@tasks_routes.route('/tasks', methods=['GET'])
@user_login_required
def fetch_tasks():
    """Fetch all tasks."""
    task = tasks.get_all_tasks()
    now = timezone.convert_utc_to_thailand_time(datetime.now())
    users = app.service.user.get_all_users()
    print(f"Users: {users}")

    return render_template('tasks.html', task_data=task, today=now, users=users)


@tasks_routes.route('/tasks/add', methods=['GET', 'POST'])
@user_login_required
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


@tasks_routes.route('/tasks/edit', methods=['GET','POST'])
@user_login_required

def edit_task():
    """Edit an existing task."""
    task_id = request.form.get('id')
    name = request.form.get('name')
    due_date = request.form.get('due_date')
    status = request.form.get('status')
    assigned_to = request.form.get('assigned-to')

    print(f" task_id: {task_id} name: {name} due_date: {due_date} status: {status} assigned_to: {assigned_to}")

    try:
        tasks.update_task(task_id, name, due_date, status, assigned_to)
        return jsonify({'message': 'Task updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tasks_routes.route('/tasks/delete', methods=['POST'])
@user_login_required
def delete_task():
    """Delete a task."""
    task_id = request.form.get('id')

    try:
        tasks.delete_task(task_id)
        return jsonify({'message': 'Task deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tasks_routes.route('/tasks/update-status', methods=['POST'])
@user_login_required
def update_task_status():
    data = request.get_json()  # Access JSON data
    task_id = data.get('id')
    status = data.get('status')

    print(f"Updating task {task_id} status to {status}")

    try:
        tasks.update_task_status(task_id, status=status)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
