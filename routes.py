from flask import Blueprint, render_template, redirect, url_for, request, session
from Utils import auth, user

routes = Blueprint("routes", __name__)  # Create a Blueprint

def user_login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("routes.login"))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Preserve function name
    return wrap

def admin_login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("routes.login"))  # Redirect to login page if not logged in
        if user.get_role_by_username(session["user"]) != "Admin":
            return redirect(url_for("routes.dashboard"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Preserve function name
    return wrap

@routes.route('/')
def home():
    return "Welcome! <a href='/dashboard'>Go to Dashboard</a>"

@routes.route('/dashboard')
@user_login_required
def dashboard():
    return render_template('home.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if auth.login(username, password):
            print("Login successful")
            session["user"] = username
            return redirect(url_for("routes.dashboard"))
    return render_template('login.html')

@routes.route('/logout')
@user_login_required
def logout():
    session.pop("user", None)
    return redirect(url_for("routes.login"))

@routes.route('/usermanagement', methods=['GET', 'POST']) # wil have to create page for members and adding
@admin_login_required
def add_user():
    return render_template('users.html')

@routes.route('/task', methods=['GET', 'POST'])
@user_login_required
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('routes.home'))  # Use Blueprint name

    return render_template('task.html')

@routes.route('/inventory', methods=['GET', 'POST'])
@user_login_required
def inventory():
    return render_template('inventory.html')