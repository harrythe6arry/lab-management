from flask import Blueprint, render_template, redirect, url_for, request
from Utils import auth, user, db  # Importing db as a module

routes = Blueprint("routes", __name__)  # Create a Blueprint

@routes.route('/inventory', methods=['GET', 'POST'])
def inventory():
    return render_template('inventory.html')

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('routes.home'))  # Use Blueprint name

    return render_template('task.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")
        if auth.login(username, password):
            print("Login successful")
        return redirect(url_for('routes.home'))  # Use Blueprint name
    return render_template('login.html')

@routes.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user.insert_user(username, password, 'Staff')
    return render_template('signup.html')

@routes.route('/equipment')
def equipment():
    conn = db.get_db_connection
    cur = conn.cursor()
    cur.execute('SELECT id, name, status, last_cleaned_at, location FROM equipment;')
    equipment_list = cur.fetchall()
    cur.close()
    db.close_db_connection(conn)

    return render_template('equipment.html', equipment_list=equipment_list)