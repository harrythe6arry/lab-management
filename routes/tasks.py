from flask import render_template, redirect, url_for, request, Blueprint, session
from .auth import user_login_required

tasks_routes = Blueprint("tasks_routes", __name__)

@tasks_routes.route('/task', methods=['GET', 'POST'])
@user_login_required
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('routes.home'))

    return render_template('task.html')